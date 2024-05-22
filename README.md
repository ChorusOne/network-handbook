# The Network Handbook

This repository contains the Chorus One _Network Handbook_, a book that
consolidates our learnings as a node operator about reliably operating blockchain
networks at scale. The goal of this book is to help networks take the quality of
their node software and operational procedures to the next level, to help build
stable and mature mainnets.

You can read the book at <https://handbook.chorus.one>.

## Building

The book is built with [mdBook][mdBook], see the upstream documentation for more
details. To start a local preview server:

    mdbook serve

The exact version of mdBook to use is listed in the `mdbook-version` file.

[mdBook]: https://rust-lang.github.io/mdBook/index.html

## Contributing

 * TODO: Are we open to external contributions?
 * Please put every sentence on its own line, and break long sentences across
   multiple lines. This ensures that diffs are easy to review on GitHub. Try to
   keep it under 80 columns if possible, but break at a logical point, don't fill
   up the line. (If we would fill up the line, a small change can cause the
   entire paragraph to re-flow, which pollutes the diff.)
 * In a list of best practices, prefer level-4 headings (`####`) per item over
   using an enumeration. This facilitates linking to individual recommendations.

## License

This book is licensed under the [Creative Commons BY-NC-SA 4.0][license] license.

[license]: https://creativecommons.org/licenses/by-nc-sa/4.0/
