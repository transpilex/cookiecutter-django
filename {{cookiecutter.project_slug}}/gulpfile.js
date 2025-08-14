const {series, src, dest, parallel, watch} = require("gulp");

const autoprefixer = require("gulp-autoprefixer");
const concat = require("gulp-concat");
const CleanCSS = require("gulp-clean-css");
const rename = require("gulp-rename");
const rtlcss = require("gulp-rtlcss");
const sourcemaps = require("gulp-sourcemaps");
const sass = require("gulp-sass")(require("sass"));

{%- if cookiecutter.plugins_config == 'y' -%}
const pluginFile = require("./plugins.config"); // Import the plugins list
{%- endif %}


const paths = {
    baseDistAssets: "{{ cookiecutter.project_slug }}/static/", // build assets directory
    baseSrcAssets: "{{ cookiecutter.project_slug }}/static/",   // source assets directory
};


{%- if cookiecutter.plugins_config == 'y' -%}
// Copying Third Party Plugins Assets
const plugins = function () {
    const out = paths.baseDistAssets + "plugins/";

    pluginFile.forEach(({name, vendorsJS, vendorCSS, vendorFonts, assets, fonts, font, media, img, webfonts}) => {

        const handleError = (label, files) => (err) => {
            const shortMsg = err.message.split('\n')[0];
            console.error(`\n${label} - ${shortMsg}`);
            throw new Error(`${label} failed`);
        };

        if (vendorsJS) {
            src(vendorsJS)
                .on('error', handleError('vendorsJS'))
                .pipe(concat("vendors.min.js"))
                .pipe(dest(paths.baseDistAssets + "js/"));
        }

        if (vendorCSS) {
            src(vendorCSS)
                .pipe(concat("vendors.min.css"))
                .on('error', handleError('vendorCSS'))
                .pipe(dest(paths.baseDistAssets + "css/"));
        }

        if (vendorFonts) {
            src(vendorFonts)
                .on('error', handleError('vendorFonts'))
                .pipe(dest(paths.baseDistAssets + "css/fonts/"));
        }

        if (assets) {
            src(assets)
                .on('error', handleError('assets'))
                .pipe(dest(`${out}${name}/`));
        }

        if (img) {
            src(img)
                .on('error', handleError('img'))
                .pipe(dest(`${out}${name}/img/`));
        }

        if (media) {
            src(media)
                .on('error', handleError('media'))
                .pipe(dest(`${out}${name}/`));
        }


        if (fonts) {
            src(fonts)
                .on('error', handleError('fonts'))
                .pipe(dest(`${out}${name}/fonts/`));
        }

        if (font) {
            src(font)
                .on('error', handleError('font'))
                .pipe(dest(`${out}${name}/font/`));
        }

        if (webfonts) {
            src(webfonts)
                .on('error', handleError('webfonts'))
                .pipe(dest(`${out}${name}/webfonts/`));
        }
    });

    return Promise.resolve();
};
{%- endif %}


const scss = function () {
    const out = paths.baseDistAssets + "css/";

    return src(paths.baseSrcAssets + "scss/**/*.scss")
        .pipe(sourcemaps.init())
        .pipe(sass.sync().on('error', sass.logError)) // scss to css
        .pipe(
            autoprefixer({
                overrideBrowserslist: ["last 2 versions"],
            })
        )
        .pipe(dest(out))
        .pipe(CleanCSS())
        .pipe(rename({suffix: ".min"}))
        .pipe(sourcemaps.write("./")) // source maps
        .pipe(dest(out));
};


const rtl = function () {
    const out = paths.baseDistAssets + "css/";

    return src(paths.baseSrcAssets + "scss/**/*.scss")
        .pipe(sourcemaps.init())
        .pipe(sass.sync().on('error', sass.logError)) // scss to css
        .pipe(
            autoprefixer({
                overrideBrowserslist: ["last 2 versions"],
            })
        )
        .pipe(rtlcss())
        .pipe(rename({suffix: "-rtl"}))
        .pipe(dest(out))
        .pipe(CleanCSS())
        .pipe(rename({suffix: ".min"}))
        .pipe(sourcemaps.write("./")) // source maps
        .pipe(dest(out));
}


function watchFiles() {
    watch(paths.baseSrcAssets + "scss/**/*.scss", series(scss));
}

// Production Tasks
exports.default = series(
    {%- if cookiecutter.plugins_config == 'y' -%}
    plugins,
    {%- endif %}
    parallel(scss),
    parallel(watchFiles,)
);

// Build Tasks
exports.build = series(
    {%- if cookiecutter.plugins_config == 'y' -%}
    plugins,
    {%- endif %}
    parallel(scss)
);

// RTL Tasks
exports.rtl = series(
    {%- if cookiecutter.plugins_config == 'y' -%}
    plugins,
    {%- endif %}
    parallel(rtl),
    parallel(watchFiles,)
);

// RTL Build Tasks
exports.rtlBuild = series(
    {%- if cookiecutter.plugins_config == 'y' -%}
    plugins,
    {%- endif %}
    parallel(rtl),
);
