# Development Workflow

Review the Coding Standards at the bottom of this page.

In particular, please submit your own code, not LLM-generated code.  It is
fine to use an LLM to review your own code (suggested prompt: "Examining the
changes I've made, do you have suggestions on how I could improve these changes
before submitting?" or "Are any bugs present in this code?"), but note that
LLMs give answer-shaped responses without regard to truth and don't actually
think.

The main workflow:

 * Fork this repo in Github
 * Check out your repo locally and create a feature/bugfix branch for your
   changes.
 * Configure your environment (see "Install Development Tools")
 * Make your changes (make sure to add relevant tests and update the `.pyi`
   stubs, if appropriate)
 * Build the project (`uv build`)
 * Update documentation (docstrings, comments, and user-facing documentation)
 * Run tests & styling checks (see "Running Tests and Styling")
 * Check in your code to your forked copy of the repo, in a feature branch
 * Submit a PR from your feature branch to the upstream (this repo) `main`
   branch.

If you need any help with any of these steps, I encourage you to reach out
(jmaslak@antelope.net).  I want to help you and will be thrilled to know
someone is using this code! Really!

I also encourage you to reach out before making large changes, to avoid the
need for additional changes after you submit the PR.

## Install Development Tools

I am assuming you are using `uv` for modifying this project ([`uv`
installation](https://docs.astral.sh/uv/getting-started/installation/)).  If
you prefer other tools, adapt these instructions to preferred tools.

## Running Tests and Styling

Whenever you modify code, it is important to run tests.  Please do not skip
this step!

 * Run code style tests
 * Test against the current non-dev version of Python and newest versions of all
   dependencies.
 * Test against oldest supported Python version in `pyproject.toml` and oldest
   version of all dependencies.

To do this, assuming that pyproject lists Python 3.10 as the minimum version and
no release version of Python > 3.14 exists yet:
```
uv build
uv run mypy src
uv run stubtest range_test
uv run ruff
uv run --python=3.14 pytest
uv run --python=3.10 --resolution=lowest pytest
```

Alternatively, you can just run `sh run-tests.sh` on a Mac or Linux machine.

Correct any errors before submitting a PR.  If `ruff` detects errors outside of
the code you are modifying, it is acceptable to submit the PR with a note that
code unrelated to your changes is now failing.

## Running Code Outside of `uv`

If you want to run code outside of `uv`, you can create a virtual environment
with `uv`:
```
uv venv
```

Then you can install dependencies:
```
uv pip install --group dev .
```

You can then activate the virtual environment (instructions are for Linux/Mac):
```
source .venv/bin/activate
```

Note that this activation only works within your current terminal session. You
need to run this in each terminal session you are using for your work.

Now, you can run scripts and such from the command line.

## Coding Standards

For this project, the following coding requirements exist:

 * Follow the [code of conduct](CODE_OF_CONDUCT.md)
 * Please do not submit LLM-generated code, tets, or documentation.  See
   [CLAUDE.md](CLAUDE.md) for more information.
 * Do not break the existing API. Changes to this library should not require
   any changes in user code.  If you have a compelling reason to break the
   API, contact me at jmaslak@antelope.net.  One type of breaking change that
   might be accepted is when it is required for security reasons.
 * When making updates, the oldest Python with active security patch support
   must remain supported (I.E. Python version defined in `pyproject.toml` must
   include that version of Python)
 * It is acceptable to provide a minimum version of a dependency, but not a
   maximum version of a dependency. Do not lock dependency versions as this
   makes this library hard to install in other projects.
 * Try to keep the stub files (`.pyi` files) as readable as possible.
 * It is fine to disagree with me. Feel free to reach out if you believe these
   standards should change!
