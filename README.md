# Kai-Fa Lu — Academic Personal Website

A responsive, multi-page academic portfolio designed for GitHub Pages. The website was rebuilt from the supplied `kaifalu_page` repository and updated using the latest curriculum vitae and the supplied descriptions of two interactive resilience dashboards.

## Public URL

After deployment to the existing repository, the website will remain available at:

**https://kaifalu.github.io/page/**

## Highlights in this release

- Prominent linked affiliation cards for:
  - **CECREH · Texas Tech University** — current postdoctoral appointment
  - **iAdapt · University of Florida** — research affiliation
- Expanded **Resilient Housing, Disaster Recovery & Climate Decision Systems** program presentation.
- Two live research products integrated into the homepage and Research page:
  - **CDBG-DR Fund Dashboard** — https://kaifalu.github.io/HUD-CDBG-DR-Fund-Dashboard-Hierarchical/
  - **Climate-Housing Exposure Index Dashboard** — https://kaifalu.github.io/Climate-Housing-Exposure-Index-Dashboard/
- Dedicated dashboard case studies describing research scope, functions, audiences, and practical applications.
- Responsive dashboard layouts and optimized preview graphics for desktop, tablet, and mobile screens.

## Website structure

- `index.html` — homepage, institutional affiliations, current dashboards, research profile, selected work, recent publications, experience, and contact
- `research.html` — research themes, current CECREH program, detailed dashboard case studies, and complete project portfolio
- `publications.html` — searchable and filterable publication directory
- `activities.html` — teaching, mentoring, reviewing, institutional affiliations, awards, certificates, presentations, and technical skills
- `assets/Kaifa-Lu-CV.pdf` — latest downloadable CV
- `assets/css/styles.css` — visual design and responsive layouts
- `assets/js/main.js` — navigation, dark mode, reveal effects, and publication filters
- `assets/img/` — optimized portrait, research graphics, and dashboard previews
- `tools/build_pages.py` — optional page generator used to maintain repeated content
- `DEPLOYMENT_GUIDE.md` — detailed GitHub Pages instructions
- `CONTENT_UPDATE_GUIDE.md` — instructions for future updates

## Quick local preview

From the package root:

```bash
python preview_server.py
```

Then open `http://127.0.0.1:8000/`.

## Deployment summary

Upload **the contents of this folder** to the root of the GitHub repository `kaifalu/kaifalu_page`. In GitHub, use **Settings → Pages → Deploy from a branch → master (or main) → /(root)**.

No Jekyll, Node.js, or Python process is needed on GitHub. The `.nojekyll` file makes the site deploy as ordinary HTML, CSS, JavaScript, images, and PDF files.

## Optional page regeneration

The website is already fully generated. To regenerate the HTML pages after editing `tools/build_pages.py`:

```bash
python -m pip install -r requirements.txt
python tools/build_pages.py
```

The generated static pages can then be previewed and committed normally.
