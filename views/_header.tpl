<!DOCTYPE html>
<html
    lang="en"
    x-data="{ theme: localStorage.theme }"
    x-init="$watch('theme', updateTheme)"
>
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    % if defined("title"):
        <title>AmberELEC WebUI / {{ title }}</title>
    % else:
        <title>AmberELEC WebUI</title>
    % end
    <script src="https://unpkg.com/alpinejs" defer></script>
    <script src="https://cdn.tailwindcss.com?plugins=forms,line-clamp"></script>
    <script src="https://kit.fontawesome.com/a72d7706c6.js" crossorigin="anonymous"></script>
    <script src="https://cdn.filesizejs.com/filesize.min.js"></script>
    <script>
        if (!('themeColor' in localStorage) || !('accentColor' in localStorage)) {
            localStorage.themeColor = 'slate';
            localStorage.accentColor = 'emerald';
        }

        tailwind.config = {
            darkMode: 'class',
            theme: {
                colors: {
                    // our themed override
                    theme: tailwind.colors[localStorage.themeColor],
                    accent: tailwind.colors[localStorage.accentColor],

                    // the default colors set
                    transparent: tailwind.colors.transparent,
                    black: tailwind.colors.black,
                    white: tailwind.colors.white,
                    slate: tailwind.colors.slate,
                    gray: tailwind.colors.gray,
                    zinc: tailwind.colors.zinc,
                    neutral: tailwind.colors.neutral,
                    stone: tailwind.colors.stone,
                    red: tailwind.colors.red,
                    orange: tailwind.colors.orange,
                    amber: tailwind.colors.amber,
                    yellow: tailwind.colors.yellow,
                    lime: tailwind.colors.lime,
                    green: tailwind.colors.green,
                    emerald: tailwind.colors.emerald,
                    teal: tailwind.colors.teal,
                    cyan: tailwind.colors.cyan,
                    sky: tailwind.colors.sky,
                    blue: tailwind.colors.blue,
                    indigo: tailwind.colors.indigo,
                    violet: tailwind.colors.violet,
                    purple: tailwind.colors.purple,
                    fuchsia: tailwind.colors.fuchsia,
                    pink: tailwind.colors.pink,
                    rose: tailwind.colors.rose
                },
            },
        }

        function updateTheme(value) {
            if (value == 'dark') {
                document.documentElement.classList.add('dark');
                document.documentElement.classList.remove('light');
            } else {
                document.documentElement.classList.add('light');
                document.documentElement.classList.remove('dark');
            }
            localStorage.theme = value;
        }

        if (localStorage.theme === 'dark' || (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
            document.documentElement.classList.add('dark');
            localStorage.theme = 'dark';
        } else {
            document.documentElement.classList.add('light');
            localStorage.theme = 'light';
        }

        window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', event => {
            updateTheme(event.matches ? "dark" : "light");
        });
        function updateThemedColors(color) {
            let root = document.documentElement;

            tailwind.config.theme.colors.theme = tailwind.colors[color];

            root.style.setProperty('--scrollbar-track-dark', tailwind.colors[color][600]);
            root.style.setProperty('--scrollbar-thumb-dark', tailwind.colors[color][800]);
            root.style.setProperty('--scrollbar-track-light', tailwind.colors[color][200]);
            root.style.setProperty('--scrollbar-thumb-light', tailwind.colors[color][600]);
            root.style.setProperty('--checkers-x-dark', tailwind.colors[color][900]);
            root.style.setProperty('--checkers-y-dark', tailwind.colors[color][800]);
            root.style.setProperty('--checkers-x-light', tailwind.colors[color][500]);
            root.style.setProperty('--checkers-y-light', tailwind.colors[color][300]);
            root.style.setProperty('--star-color', tailwind.colors[color][600]);
            root.style.setProperty('--star-background', tailwind.colors[color][300]);
            root.style.setProperty('--star-color-dark', tailwind.colors[color][300]);
            root.style.setProperty('--star-background-dark', tailwind.colors[color][600]);


            localStorage.themeColor = color;
        }

        updateThemedColors(localStorage.themeColor);
    </script>
    <style>
        html, body {
            overflow-x: hidden;
            width: 100%;
            height: 100%;
        }
        body {
            font-family: sans-serif, FontAwesome;
        }

        :root {
            --scrollbar-track-dark: #475569; /* slate-600 */
            --scrollbar-thumb-dark: #1e293b; /* slate-800 */
            --scrollbar-track-light: #e2e8f0; /* slate-200 */
            --scrollbar-thumb-light: #475569; /* slate-600 */
            --checkers-x-dark: #0f172a; /* slate-900 */
            --checkers-y-dark: #1e293b; /* slate-800 */
            --checkers-x-light: #64748b; /* slate-500 */
            --checkers-y-light: #cbd5e1; /* slate-300 */
            --star-size: 20px;
            --star-color: #1e293b; /* slate-800 */
            --star-background: #94a3b8; /* slate-400 */
        }

        @font-face {
            font-family: 'DREAMS';
            src: url('/assets/fonts/DREAMS.woff2') format('woff2'),
                url('/assets/fonts/DREAMS.woff') format('woff');
            font-weight: normal;
            font-style: normal;
            font-display: swap;
        }

        @media (prefers-color-scheme: dark) {
            .checkers {
                background: repeating-conic-gradient(var(--checkers-x-dark) 0% 25%, var(--checkers-y-dark) 0% 50%) 50% / 20px 20px;
            }
            .light .checkers {
                background: repeating-conic-gradient(var(--checkers-x-light) 0% 25%, var(--checkers-y-light) 0% 50%) 50% / 20px 20px;
            }
        }

        @media (prefers-color-scheme: light) {
            .checkers {
                background: repeating-conic-gradient(var(--checkers-x-light) 0% 25%, var(--checkers-y-light) 0% 50%) 50% / 20px 20px;
            }
            .dark .checkers {
                background: repeating-conic-gradient(var(--checkers-x-dark) 0% 25%, var(--checkers-y-dark) 0% 50%) 50% / 20px 20px;
            }
        }

        .dark ::-webkit-scrollbar {
            width: 14px;
            height: 3px;
            padding: 2px;
        }
        .dark ::-webkit-scrollbar-track-piece {
            background-color: var(--scrollbar-track-dark); ; /* slate-600 */
        }
        .dark ::-webkit-scrollbar-thumb {
            height: 50px;
            background-color: var(--scrollbar-thumb-dark); /* slate-800 */
            background-clip: padding-box;
            border-radius: 99px;
            border: 3px solid rgba(0, 0, 0, 0);
        }

        .light ::-webkit-scrollbar {
            width: 14px;
            height: 3px;
            padding: 2px;
        }
        .light ::-webkit-scrollbar-track-piece {
            background-color: var(--scrollbar-track-light);
        }
        .light ::-webkit-scrollbar-thumb {
            height: 50px;
            background-color: var(--scrollbar-thumb-light); /* slate-600 */
            background-clip: padding-box;
            border-radius: 99px;
            border: 3px solid rgba(0, 0, 0, 0);
        }

        .stars {
            --percent: calc(var(--rating) / 5 * 100%);
            display: inline-block;
            font-size: var(--star-size);
            font-family: Times;
            line-height: 1;
        }

        .stars::before {
            content: '★★★★★';
            letter-spacing: 3px;
            background: linear-gradient(90deg, var(--star-color-dark) var(--percent), var(--star-background-dark) var(--percent));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            text-fill-color: transparent;
        }

        .light .stars::before {
            content: '★★★★★';
            letter-spacing: 3px;
            background: linear-gradient(90deg, var(--star-color) var(--percent), var(--star-background) var(--percent));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            text-fill-color: transparent;
        }


        input[type=search]::-ms-clear { display: none; width : 0; height: 0; }
        input[type=search]::-ms-reveal { display: none; width : 0; height: 0; }
        input[type="search"]::-webkit-search-decoration,
        input[type="search"]::-webkit-search-cancel-button,
        input[type="search"]::-webkit-search-results-button,
        input[type="search"]::-webkit-search-results-decoration { display: none; }
    </style>
    <style>
        .rating {
            --dir: right;
            --fill: var(--star-color-dark);
            --fillbg: var(--star-background-dark);
            --heart: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M12 21.328l-1.453-1.313q-2.484-2.25-3.609-3.328t-2.508-2.672-1.898-2.883-0.516-2.648q0-2.297 1.57-3.891t3.914-1.594q2.719 0 4.5 2.109 1.781-2.109 4.5-2.109 2.344 0 3.914 1.594t1.57 3.891q0 1.828-1.219 3.797t-2.648 3.422-4.664 4.359z"/></svg>');
            --star: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M12 17.25l-6.188 3.75 1.641-7.031-5.438-4.734 7.172-0.609 2.813-6.609 2.813 6.609 7.172 0.609-5.438 4.734 1.641 7.031z"/></svg>');
            --stars: 5;
            --starsize: 2rem;
            --symbol: var(--star);
            --value: 1;
            --w: calc(var(--stars) * var(--starsize));
            --x: calc(100% * (var(--value) / var(--stars)));
            block-size: var(--starsize);
            inline-size: var(--w);
            position: relative;
            touch-action: manipulation;
            -webkit-appearance: none;
            background: transparent;
        }

        .light .rating {
            --fill: var(--star-color);
            --fillbg: var(--star-background);
        }

        [dir="rtl"] .rating {
            --dir: left;
        }
        .rating::-moz-range-track {
            background: linear-gradient(to var(--dir), var(--fill) 0 var(--x), var(--fillbg) 0 var(--x));
            block-size: 100%;
            mask: repeat left center/var(--starsize) var(--symbol);
        }
        .rating::-webkit-slider-runnable-track {
            background: linear-gradient(to var(--dir), var(--fill) 0 var(--x), var(--fillbg) 0 var(--x));
            block-size: 100%;
            mask: repeat left center/var(--starsize) var(--symbol);
            -webkit-mask: repeat left center/var(--starsize) var(--symbol);
        }
        .rating::-moz-range-thumb {
            height: var(--starsize);
            opacity: 0;
            width: var(--starsize);
        }
        .rating::-webkit-slider-thumb {
            height: var(--starsize);
            opacity: 0;
            width: var(--starsize);
            -webkit-appearance: none;
        }
        .rating, .rating-label {
            display: block;
        }
    </style>
    <style type="text/tailwindcss">
        @layer components {
            .form-input {
                @apply
                    flex-1 block w-full
                    focus:ring-theme-500
                    focus:border-accent-500
                    dark:focus:border-accent-400
                    border-theme-400
                    rounded-md
                    shadow-sm
                    sm:text-sm
                    text-theme-800 dark:text-theme-300
                    placeholder-theme-400 dark:placeholder-theme-500
                    bg-theme-200 dark:bg-theme-700
            }
        }

    </style>
</head>
<body class="dark:bg-theme-900 bg-gradient-to-br from-theme-50 dark:from-theme-800 to-theme-100 dark:to-theme-900 transform duration-200 ease-in-out">
% if get('search', False):
<div x-data="load_search_data()" class="container mx-auto max-w-[1200px] p-5">
% else:
<div class="container mx-auto max-w-[1200px] p-5">
% end
    <div class="grid grid-cols-2 mb-5">
        <div class="col-span-1 grow h-20">
            <a href="/">
                % include('_logo')
            </a>
        </div>
        <div class="col-span-1 grid grid-rows-2">
            <div class="self-center flex justify-end justify-self-end items-center space-x-2">
                <span class="text-sm text-theme-800 dark:text-theme-500"><svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
                    </svg></span>
                <label for="toggle" class="w-9 h-5 flex items-center bg-theme-300 rounded-full p-1 cursor-pointer duration-300 ease-in-out dark:bg-theme-600">
                    <div class="toggle-dot bg-white w-4 h-4 rounded-full shadow-md transform duration-300 ease-in-out dark:translate-x-3"></div>
                </label>
                <span class="text-sm text-theme-400 dark:text-white"><svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
                    </svg></span>
                <input id="toggle" type="checkbox" class="hidden" :value="theme" @change="theme = (theme == 'dark' ? 'light' : 'dark')" />
                <div class="pr-5">
                    <div x-data="{
                            selected: 'slate',
                            colors: [
                                'slate', 'gray', 'zinc', 'neutral', 'stone', 'red', 'orange', 'amber', 'yellow', 'lime', 'green',
                                'emerald', 'teal', 'cyan', 'sky', 'blue', 'indigo', 'violet', 'purple', 'fuchsia', 'pink', 'rose'
                            ],
                            picking: false
                        }"
                        x-init="$watch('selected', value => updateThemedColors(value))"
                        class="relative">
                        <i x-on:click="picking = !picking" class="fa-solid fa-palette text-theme-500"></i>
                        <div x-show="picking" class="absolute grid grid-cols-11 gap-1 w-[250px] p-2 right-0 top-9 bg-theme-100 bg-opacity-50 shadow-md backdrop-blur rounded">
                            <template x-for="color in colors">
                                <div x-on:click="selected = color" class="cursor-pointer w-[20px] h-[20px] rounded-lg border border-2 relative" :class="`bg-${color}-500 border-${color}-600`">&nbsp;</div>
                            </template>
                        </div>
                    </div>
                </div>
            </div>
            <div class="w-1/2 self-center flex justify-end justify-self-end items-center space-x-2">
                % if get('actions', False):
                    % for text, href in actions.items():
                        <a class="text-accent-100 bg-accent-600 rounded-lg text-xs font-medium focus:outline-none p-1.5 px-2 cursor-pointer border border-transparent" href="{{ href }}">{{ text }}</a>
                    % end
                % end
                % if get('search', False):
                    <input
                        x-ref="searchField"
                        x-model="search"
                        x-on:keydown.window.prevent.slash="$refs.searchField.focus()"
                        placeholder="Search..."
                        type="search"
                        class="form-input self-end justify-self-end w-1/2 flex text-xs p-1.5 px-2"
                    />
                % end
            </div>

        </div>
    </div>

    <div class="text-theme-200 bg-theme-700 dark:bg-theme-700 rounded-lg text-xs font-medium uppercase tracking-wide p-2 px-3 mb-5">
        % for text, href in nav.items():
            <a href="{{ href }}">{{ text }}</a>
            % if list(nav)[-1] != text:
                /
            % end
        % end

        <a href="/reloadgames" title="Refresh Gamelist" x-on:click.prevent="fetch('/reloadgames').then(() => location.reload())" class="inline float-right"><i class="fas fa-sync"></i></a>
    </div>
