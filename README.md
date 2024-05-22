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
 * For listing best practices, use a level-4 heading (`####`), so that we have
   an anchor to link to. Apply one of the p0–p3 classes to indicate priority
   by adding `{.p0}` at the end of the heading. Use a custom anchor to ensure
   that links remain stable even if we rephrase the advice. See also [heading
   attributes][heading-attributes] in mdBook.

[heading-attributes]: https://rust-lang.github.io/mdBook/format/markdown.html#heading-attributes

## License

This book is licensed under the [Creative Commons BY-NC-SA 4.0][license] license.

[license]: https://creativecommons.org/licenses/by-nc-sa/4.0/
