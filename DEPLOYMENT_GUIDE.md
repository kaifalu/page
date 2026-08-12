# GitHub Pages Deployment Guide

## 1. Back up the current repository

Before replacing the existing website, download the current repository as a ZIP or create a backup branch in GitHub. This makes it easy to restore the older Jekyll version when needed.

## 2. Extract this package

Extract the final ZIP on your computer. Open the extracted folder and confirm that `index.html`, `research.html`, `publications.html`, `activities.html`, `.nojekyll`, and the `assets` folder are directly inside it.

Do not upload the outer ZIP or an unnecessary parent folder. GitHub Pages must find `index.html` at the repository root.

## 3. Replace the repository contents

For the existing repository `kaifalu/kaifalu_page`:

1. Remove the outdated Jekyll pages and layouts after preserving a backup.
2. Upload all files and folders from this package to the repository root.
3. Commit the update with a message such as `Redesign website and update from 2026 CV`.

A command-line alternative is:

```bash
git clone https://github.com/kaifalu/kaifalu_page.git
cd kaifalu_page
# Copy the contents of this package into the cloned folder.
git add --all
git commit -m "Redesign website and update from latest CV"
git push origin master
```

Use `main` instead of `master` when that is the repository's default branch.

## 4. Configure GitHub Pages

Open the repository in GitHub and select:

1. **Settings**
2. **Pages**
3. **Build and deployment**
4. **Source: Deploy from a branch**
5. **Branch: master** or **main**
6. **Folder: /(root)**
7. **Save**

The permanent address remains:

**https://kaifalu.github.io/kaifalu_page/**

## 5. Check the deployment

After GitHub finishes publishing, verify:

- the homepage loads without a 404 error;
- Research, Publications, and Activities open correctly;
- the latest CV opens from the header and contact section;
- publication filters and search work;
- light/dark mode works;
- the mobile menu opens on a narrow screen;
- images display correctly;
- old routes such as `/publications/` and `/research/` redirect to the redesigned pages.

## 6. Local preview before publishing

Run:

```bash
python preview_server.py
```

Open `http://127.0.0.1:8000/` in a browser. This is preferable to opening `index.html` directly because it reproduces normal website behavior more accurately.

## 7. Troubleshooting

### The old webpage still appears

Use a hard refresh (`Ctrl+F5` on Windows or `Cmd+Shift+R` on macOS). Also confirm that GitHub Pages is deploying the branch and root folder containing the new `index.html`.

### Images or CSS are missing

Confirm that the complete `assets` folder was uploaded and that capitalization was preserved. GitHub Pages paths are case-sensitive.

### The CV is outdated

Replace `assets/Kaifa-Lu-CV.pdf` with the new PDF while keeping the same filename. Existing links will continue to work.

### The site is nested under another folder

Move `index.html`, `.nojekyll`, and `assets` to the repository root. Do not leave them only inside a package subfolder.

## 8. Verify the new affiliation and dashboard integrations

After deployment, confirm that:

- the homepage hero and Institutional Affiliations section link to CECREH at Texas Tech University and iAdapt at the University of Florida;
- the Research page identifies CECREH as the current appointment and iAdapt as the research affiliation;
- both dashboard preview cards open the correct live applications in new tabs;
- the CDBG-DR case study displays the 2001–2023 scope, 18 categories, 40 states and U.S. territories, and seven hierarchical filters;
- the Climate-Housing case study displays the 1.5°C–3.0°C scenarios, 2020–2050 growth comparison, CHEI, and compound-hotspot functions;
- the dashboard cards stack cleanly on a phone-sized screen without horizontal scrolling.
