//! The {{ name or devset.target }} command line.

fn main() {
    {{ (name or devset.target) | replace("-", "_") }}::run();
}
