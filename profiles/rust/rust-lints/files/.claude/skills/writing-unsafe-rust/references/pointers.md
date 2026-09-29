{%- set toolchain = devset.layers | selectattr("profile", "equalto", "rust-toolchain") | map(attribute="features") | first | default([]) -%}
# Pointers

Read this before a raw pointer is made, cast, offset or dereferenced, before a
pointer becomes an integer or an integer a pointer, before `transmute`,
`MaybeUninit` or `mem::zeroed`, and before an `extern` block or an exported
symbol. It says how a pointer keeps the right to reach what it points at, and
what each conversion must prove.

A pointer is an address and a provenance: the memory it may reach, and for how
long. A pointer derived from a reference or an allocation inherits that one's
provenance, and nothing can widen it. The standard library's strict provenance
functions keep the two apart, so no pointer's provenance is ever guessed.

## An Address Is `addr()`, Never `as usize`

A cast from a pointer to an integer with `as` exposes the pointer's provenance
to a table the compiler must then assume anything may draw on, which costs
optimizations and hampers the tools that check provenance. `addr()` reads the
address alone. An address changed and put back, as a tag in the spare low bits
of an aligned pointer, is `map_addr(|addr| addr | 1)`, which keeps the
provenance; a pointer that is never dereferenced, a sentinel or an address a
test needs, is `ptr::without_provenance(addr)`, and an aligned one that is never
read is `NonNull::dangling()`.
{%- if "nightly" in devset.features %}

```rust,compile_fail
// fails: implicit_provenance_casts
#[must_use]
pub fn aligned(squares: &[u8]) -> bool {
    // Bad: the cast exposes the pointer's provenance, to read an address.
    (squares.as_ptr() as usize).is_multiple_of(64)
}
```
{%- endif %}

```rust
#[must_use]
pub fn aligned(squares: &[u8]) -> bool {
    squares.as_ptr().addr().is_multiple_of(64)
}
```

Held by review.
{%- if "nightly" in devset.features %}

Under `nightly`, `implicit_provenance_casts` refuses an `as` cast between a
pointer and an integer, either way.
{%- endif %}
{%- if "strict" in devset.features %}

Under `strict`, `clippy::as_conversions` refuses every `as`.
{%- endif %}

## Rebuild a Pointer from One Whose Provenance Covers the Place

A pointer made from a reference reaches what that reference covers and no
further: one from `&squares[3]` reaches one square, and a read of the square
after it is undefined behaviour however the address checks out. A pointer that
must reach around the place a handle names takes the handle's address and the
owner's provenance, `base.with_addr(handle.addr())`, where `base` is the owner's
own pointer; `add` and `byte_add` then offset within the owner. Where the owner
is a slice, `get(offset)` does the same with no unsafe at all; `with_addr` is
for an owner that is itself a pointer: a mapping, an allocation, a header before
its payload.

```rust
use core::ptr::NonNull;

#[derive(Debug)]
pub struct Grid {
    squares: Box<[u8]>,
}

impl Grid {
    #[must_use]
    pub fn square(&self, at: usize) -> Option<NonNull<u8>> {
        self.squares.get(at).map(NonNull::from)
    }

    /// The square after `square`.
    ///
    /// # Safety
    /// `square` came from `square` on this grid, and is not its last.
    #[expect(unsafe_code, reason = "a read of the square after one a handle names")]
    #[must_use]
    pub const unsafe fn after(&self, square: NonNull<u8>) -> u8 {
        // SAFETY: the caller promises a square of this grid that is not its last, so the square
        // after it is one too.
        let next = unsafe { square.add(1) };
        // Bad: `square` came from a `&u8`, whose provenance covers that square alone.
        // SAFETY: as above.
        unsafe { next.read() }
    }
}
```

```rust
use core::ptr::NonNull;

#[derive(Debug)]
pub struct Grid {
    squares: Box<[u8]>,
}

impl Grid {
    #[must_use]
    pub fn square(&self, at: usize) -> Option<NonNull<u8>> {
        self.squares.get(at).map(NonNull::from)
    }

    #[must_use]
    pub fn after(&self, square: NonNull<u8>) -> Option<u8> {
        let base = NonNull::from(&*self.squares).cast::<u8>();
        let next = square.addr().checked_add(1)?;
        let offset = next.get().checked_sub(base.addr().get())?;
        if offset >= self.squares.len() {
            return None;
        }
        // SAFETY: `with_addr` gives `next` the provenance of every square, which are live and
        // initialized for `&self`, and `offset` is below their count, checked above.
        #[expect(unsafe_code, reason = "a read at an address a handle names, on the grid's own provenance")]
        Some(unsafe { base.with_addr(next).read() })
    }
}
```

Held by review.
{%- if "miri" in toolchain %}

Miri refuses the read, under the tests that reach it, as `verifying.md` shows.
{%- endif %}

## Exposed Provenance Is for an Address from Outside the Program

`expose_provenance` and `with_exposed_provenance` are what an `as` cast between
a pointer and an integer means, said as a call. They are for an address the
program did not allocate, a device register at a fixed address, which counts as
exposed, or a foreign interface that hands a pointer back only as an integer,
exposed on the way out. Rebuilt from a bare integer, a pointer's provenance is
whichever exposed one the compiler picks, and undefined behaviour if none covers
the use. Inside the program a pointer keeps its type: a field, an argument or an
`AtomicPtr`, never an address saved to be turned back.

```rust
use core::ptr;

#[derive(Debug)]
pub struct Cursor {
    // Bad: an address that dropped its provenance, so the read below guesses which it had.
    at: usize,
}

impl Cursor {
    #[must_use]
    pub fn new(square: &u8) -> Self {
        Self { at: ptr::from_ref(square).expose_provenance() }
    }

    /// The square the cursor is on.
    ///
    /// # Safety
    /// The square `new` took is still live.
    #[expect(unsafe_code, reason = "a read at the address the cursor keeps")]
    #[must_use]
    pub const unsafe fn square(&self) -> u8 {
        let square = ptr::with_exposed_provenance::<u8>(self.at);
        // SAFETY: the caller promises the square is live, and `new` exposed its provenance.
        unsafe { square.read() }
    }
}
```

```rust
use core::ptr;

/// The tile display's status register, which the board's memory map fixes.
const STATUS: usize = 0x4000_1000;

/// The display's status word.
///
/// # Safety
/// The display is mapped at `STATUS`, as on the board this crate is built for.
#[expect(unsafe_code, reason = "a read of a device register at a fixed address")]
#[must_use]
pub unsafe fn status() -> u32 {
    let register = ptr::with_exposed_provenance::<u32>(STATUS);
    // SAFETY: the caller promises the display is mapped at `STATUS`, memory outside the program
    // counts as exposed, and the register is aligned for a `u32`.
    unsafe { register.read_volatile() }
}
```

Held by review.
{%- if "nightly" in devset.features %}

Under `nightly`, `implicit_provenance_casts` refuses the `as` spelling of
either, so each is written as the call it is.
{%- endif %}
{%- if "miri" in toolchain %}

Miri under `-Zmiri-strict-provenance` refuses `with_exposed_provenance`, which
is how a test finds a round trip inside the program.
{%- endif %}

## Cast with `cast` and `&raw`, and Write Only Through a Pointer from a `&mut`

`as` between pointers changes the pointee type, the mutability and, to or from
an integer, the provenance, and says nothing of which it meant. Each has its own
spelling: `cast::<T>()` changes the type, `cast_mut` and `cast_const` the
mutability, `ptr::from_ref` and `ptr::from_mut` take a reference, and `&raw
const place` or `&raw mut place` a place that must not be referenced: a field of
a packed struct, or one not yet initialized. A pointer is written through only
where it came from a `&mut` or from the owner: one from a shared borrow may not
be written outside an `UnsafeCell`, and `cast_mut` does not change that; it is
for an interface that takes `*mut` and never writes, as `AtomicPtr` does.

```rust,compile_fail
// fails: clippy::ptr_cast_constness
#[expect(unsafe_code, reason = "a write through the row's base")]
pub fn clear_first(row: &[u8]) {
    if row.is_empty() {
        return;
    }
    // Bad: a pointer from a shared borrow, which may never be written through.
    let base = row.as_ptr() as *mut u8;
    // SAFETY: the row is not empty.
    unsafe {
        base.write(0);
    }
}
```

```rust
#[expect(unsafe_code, reason = "a write through the row's base")]
pub const fn clear_first(row: &mut [u8]) {
    if row.is_empty() {
        return;
    }
    let base = row.as_mut_ptr();
    // SAFETY: the row is not empty, and `&mut` makes its first square this call's to write.
    unsafe {
        base.write(0);
    }
}
```

Held by `clippy::ptr_as_ptr`, `ptr_cast_constness`, `borrow_as_ptr` and
`ref_as_ptr`, which refuse the `as` forms; a write through a shared borrow's
pointer, spelled with `cast_mut`, is held by review.
{%- if "strict" in devset.features %}

Under `strict`, `clippy::as_ptr_cast_mut` refuses `as_ptr() as *mut`, and
`clippy::as_conversions` every `as`.
{%- endif %}

## A Reference Made from a Pointer Holds for All of Its Lifetime

A reference promises, for as long as it lives, that its pointer is non-null,
aligned and points at a valid, initialized value; a `&T` that nothing writes the
value outside an `UnsafeCell`, and a `&mut T` that nothing else reads or writes
it. So a reference made from a pointer gets its lifetime from a borrow the
signature shows, `&self` giving `&'_ T`, never an unbounded `'a` a caller picks,
and a `&mut` comes only from a `&mut`: a `&mut` from `&self` lets two callers
hold one each.

```rust,compile_fail
// fails: clippy::mut_from_ref
use core::cell::UnsafeCell;

#[derive(Debug)]
pub struct Board {
    squares: UnsafeCell<[u8; 9]>,
}

impl Board {
    // Bad: two calls give two `&mut` of the same squares.
    #[expect(unsafe_code, reason = "the squares, for a caller to change")]
    #[must_use]
    pub const fn squares(&self) -> &mut [u8; 9] {
        // SAFETY: the board is alive for as long as `&self`.
        unsafe { &mut *self.squares.get() }
    }
}
```

```rust
#[derive(Debug)]
pub struct Board {
    squares: [u8; 9],
}

impl Board {
    #[must_use]
    pub const fn squares_mut(&mut self) -> &mut [u8; 9] {
        &mut self.squares
    }
}
```

Held by `clippy::mut_from_ref`, which refuses a `&mut` returned from only shared
borrows, and by review for the rest.

## No `transmute`: Name the Conversion

`transmute` reinterprets bytes and checks only that the sizes agree: not byte
order, not that every pattern is a valid value of the target, not alignment, not
lifetimes. A named conversion says what it means and checks what it can:
`from_le_bytes` and `to_le_bytes` with the byte order stated, `f32::from_bits`,
`cast` between pointers, `ptr::from_ref`, a `TryFrom` or a `match` for an enum
from its discriminant, and a derive that proves a type's layout where the
workspace has one, as zerocopy's does. A `transmute` that remains names both
types, `transmute::<A, B>`, and its `// SAFETY:` proves every pattern valid for
the target, the alignment and the lifetimes.

```rust,compile_fail
// fails: unnecessary_transmutes
use core::mem;

#[expect(unsafe_code, reason = "four squares read as one word")]
#[must_use]
pub const fn packed(squares: [u8; 4]) -> u32 {
    // Bad: says nothing of byte order.
    // SAFETY: any four bytes are a `u32`.
    unsafe { mem::transmute::<[u8; 4], u32>(squares) }
}
```

```rust
#[must_use]
pub const fn packed(squares: [u8; 4]) -> u32 {
    u32::from_le_bytes(squares)
}
```

Held by `unnecessary_transmutes`, which refuses a `transmute` a safe function
does, and by clippy's `transmute_ptr_to_ref`, `transmute_ptr_to_ptr`,
`transmute_int_to_bool` and `missing_transmute_annotations`, each for the form
it names; the rest is held by review.

## Uninitialized Memory Is `MaybeUninit`, Read Only Once It Is Whole

Memory never written holds no value at all, not even an arbitrary one, so
reading it as any type is undefined behaviour, a `u8` included. `MaybeUninit<T>`
holds it until it is written; `assume_init` is called once every field is, and
not before. `mem::uninitialized` is never used; `mem::zeroed` only for a type
that all-zero bytes are a valid value of: integers, floats, raw pointers,
`Option<&T>`, not a reference, a `NonNull`, a `NonZero` or a function pointer.
An array of slots is `[const { MaybeUninit::uninit() }; N]`, a `Vec`'s spare
room is `spare_capacity_mut`, counted with `set_len` once written, and where
`array::from_fn` or `extend` builds the value, neither is needed.

```rust,compile_fail
// fails: clippy::uninit_assumed_init
use core::mem::MaybeUninit;

#[expect(unsafe_code, reason = "a row filled after it is made")]
#[must_use]
pub fn row() -> [u8; 8] {
    // Bad: eight bytes never written, read as eight `u8`s.
    // SAFETY: a `u8` has no invalid bit pattern.
    let mut row: [u8; 8] = unsafe { MaybeUninit::uninit().assume_init() };
    for (tile, square) in (0_u8..).zip(&mut row) {
        *square = tile;
    }
    row
}
```

```rust
use core::mem::MaybeUninit;

#[derive(Debug)]
pub struct Tile {
    pub label: String,
}

#[must_use]
pub fn row(label: &str) -> [Tile; 8] {
    let mut row = [const { MaybeUninit::<Tile>::uninit() }; 8];
    for slot in &mut row {
        slot.write(Tile { label: label.to_owned() });
    }
    // SAFETY: the loop wrote every slot; had it panicked, the slots would have leaked what they
    // held, since a `MaybeUninit` drops nothing.
    #[expect(unsafe_code, reason = "a row whose every slot the loop above wrote")]
    unsafe { MaybeUninit::<[Tile; 8]>::from(row).assume_init() }
}
```

Held by `clippy::uninit_assumed_init` and `clippy::uninit_vec`, and by rustc's
`invalid_value`, which refuses `mem::zeroed` or `mem::uninitialized` of a type
it can see they are wrong for; the rest is held by review.

## An `extern` Block Is `unsafe extern`, and Each Call Proves What C Asks

The compiler cannot check a foreign declaration, so an `extern` block is `unsafe
extern`, which edition 2024 requires, and each item in it is `unsafe` to call
unless marked `safe fn`, a promise that no argument value can make the call
unsound: `getpid` qualifies, and `abs` does not, since `abs(INT_MIN)` is
undefined in C. A function that takes a pointer stays unsafe, and a safe wrapper
passes only pointers it derived from references it holds for the call: a
`CString` is bound to a name before its pointer is taken, since a temporary's
pointer dangles at the end of its statement. An exported symbol is
`#[unsafe(no_mangle)]` or `#[unsafe(export_name = "…")]`, a promise that no
other symbol of the program has its name, and a type that crosses is
`#[repr(C)]` and spelled with `core::ffi`'s types.

```rust,compile_fail
// fails: dangling_pointers_from_temporaries
extern crate alloc;

use alloc::ffi::{CString, NulError};
use core::ffi::c_char;

#[expect(unsafe_code, reason = "the C library's `strlen`, which reads up to a NUL")]
unsafe extern "C" {
    fn strlen(label: *const c_char) -> usize;
}

pub fn label_len(label: &str) -> Result<usize, NulError> {
    // Bad: the `CString` is dropped at the end of this line, and the pointer dangles.
    let label = CString::new(label)?.as_ptr();
    // SAFETY: `label` is NUL-terminated.
    #[expect(unsafe_code, reason = "a C call over a label")]
    Ok(unsafe { strlen(label) })
}
```

```rust
extern crate alloc;

use alloc::ffi::{CString, NulError};
use core::ffi::c_char;

#[expect(unsafe_code, reason = "the C library's `strlen`, which reads up to a NUL")]
unsafe extern "C" {
    fn strlen(label: *const c_char) -> usize;
}

pub fn label_len(label: &str) -> Result<usize, NulError> {
    let label = CString::new(label)?;
    // SAFETY: a `CString` is NUL-terminated, and `label` lives past the call, which only reads
    // it.
    #[expect(unsafe_code, reason = "a C call over a label this function holds")]
    Ok(unsafe { strlen(label.as_ptr()) })
}
```

Held by `dangling_pointers_from_temporaries`, which refuses a pointer taken from
a temporary that is dropped at once, by the compiler, which refuses a bare
`extern` block, `#[no_mangle]` or `#[export_name]` in edition 2024, and by
review for a `safe fn` and for what each call proves.
