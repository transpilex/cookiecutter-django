import {defineConfig} from 'vite';
import {globSync} from 'glob';

{%- if cookiecutter.ui_library == 'Tailwind' %}
import tailwindcss from '@tailwindcss/vite';
{%- endif %}

import path from 'node:path'


export default defineConfig({
    base: '/static/',
    {%- if cookiecutter.ui_library == 'Tailwind' %}
    plugins: [
        tailwindcss()
    ],
    {%- endif %}
    build: {
        outDir: 'dist',
        manifest: true,
        rollupOptions: {
            input: Object.fromEntries(
                globSync('{{cookiecutter.project_slug}}/static/js/**/*.js').map(file => [
                    path.relative('{{cookiecutter.project_slug}}/static/js', file).replace(/\.js$/, ''),
                    file,
                ])
            )
        },
    },
});
