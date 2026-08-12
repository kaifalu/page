# Content Update Guide

The committed HTML files are ready to publish. For consistent future maintenance, edit the structured content in `tools/build_pages.py`, run the generator, preview the result, and commit the regenerated pages.

## Update the CV

Replace:

`assets/Kaifa-Lu-CV.pdf`

Keep the filename unchanged so every CV button continues to work.

## Update institutional affiliations

The current institutional links and labels appear in the homepage, Research page, Activities page, contact area, footer, and structured metadata.

For a consistent site-wide update:

1. Edit the relevant constants and template text in `tools/build_pages.py`.
2. Update the `AFFILIATIONS` list for the Activities page.
3. Update the JSON-LD `affiliation` entries in the shared page metadata when an institutional relationship changes.
4. Run `python tools/build_pages.py`.

Current official links:

- CECREH · Texas Tech University: `https://www.depts.ttu.edu/cecreh/`
- iAdapt · University of Florida: `https://dcp.ufl.edu/iadapt/`

## Update the resilience dashboards

The two dashboard records are stored in the `DASHBOARDS` list in `tools/build_pages.py`. Each record supports:

- `id`
- `title`
- `subtitle`
- `scope`
- `url`
- `image`
- `image_alt`
- `summary`
- `metrics`
- `functions`
- `audience`
- `accent`

After changing a dashboard URL, description, function, metric, or audience:

```bash
python tools/build_pages.py
```

Dashboard preview images are located at:

- `assets/img/dashboard-cdbg-fund-overview.webp`
- `assets/img/dashboard-climate-housing-overview.webp`

Replace an image while keeping its filename to avoid changing page templates. The CDBG-DR image is an illustrative interface preview; the live dashboard remains the authoritative interface.

## Update the current position or biography

Edit the relevant text in `tools/build_pages.py`, especially the homepage hero, institutional section, About section, current research program, Experience, Activities, Contact, and shared footer. Regenerate the pages afterward.

## Add a journal publication

The publication directory is generated from the `PUBLICATIONS` list in `tools/build_pages.py`.

1. Copy an existing publication dictionary.
2. Update `id`, `year`, `authors`, `title`, `venue`, `details`, `doi`, `topic`, and `status`.
3. Run:

```bash
python -m pip install -r requirements.txt
python tools/build_pages.py
```

Supported status values are `published`, `in-press`, and `review`. Topic values currently include `planning-ai`, `mobility`, `resilience`, `environment`, `policy`, and `machine-learning`.

## Update a manuscript status

When a manuscript becomes published:

1. Move its dictionary from `UNDER_REVIEW` to `PUBLICATIONS`.
2. Add final journal details and DOI.
3. Change `status` to `published` or `in-press`.
4. Regenerate the pages.

## Add or revise another project

Edit the `PROJECTS` list in `tools/build_pages.py`. Each project supports:

- date;
- role;
- title;
- image and alternative text;
- funding/source;
- description;
- bullet points.

Put new optimized images in `assets/img/` and use relative paths such as `assets/img/new-project.webp`.

## Update teaching, awards, or presentations

Edit the corresponding lists in `tools/build_pages.py`:

- `TEACHING`
- `MENTORING`
- `REVIEWERS`
- `AFFILIATIONS`
- `CERTIFICATES`
- `AWARDS`
- `PRESENTATIONS`
- `INVITED_TALKS`

Regenerate the pages afterward.

## Change colors or typography

Edit the variables at the beginning of `assets/css/styles.css`, including `--navy`, `--teal`, `--bg`, `--surface`, and `--ink`. The dark-theme variables are in the `html[data-theme="dark"]` block.

## Replace the portrait

Replace `assets/img/kai-fa-lu-profile.webp` with a new 4:5 portrait. A recommended source size is at least 1000 × 1250 pixels. Keep the filename unchanged.

## Change external profile links

Update the `SOCIALS` dictionary near the beginning of `tools/build_pages.py`, regenerate the pages, and confirm the links in the footer/contact areas.

## Regenerate and validate

```bash
python -m pip install -r requirements.txt
python tools/build_pages.py
python preview_server.py
```

Open `http://127.0.0.1:8000/` and check the homepage, Research, Publications, and Activities pages on both desktop and mobile widths before committing.
