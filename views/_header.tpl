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
        <title>351ELEC WebUI / {{ title }}</title>
    % else:
        <title>351ELEC WebUI</title>
    % end
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/alpinejs" defer></script>
    <script src="https://kit.fontawesome.com/a72d7706c6.js" crossorigin="anonymous"></script>
    <script>
        tailwind.config = {
            darkMode: 'class',
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
    </script>
    <style>
        body {
            overflow-x: hidden;
        }

        @font-face {
            font-family: 'DREAMS';
            src: url('/assets/fonts/DREAMS.woff2') format('woff2'),
                url('/assets/fonts/DREAMS.woff') format('woff');
            font-weight: normal;
            font-style: normal;
            font-display: swap;
        }

        .line-clamp {
            overflow: hidden;
            display: -webkit-box;
            -webkit-box-orient: vertical;
            -webkit-line-clamp: 6;
        }

        @media (prefers-color-scheme: dark) {
            .checkers {
                background: repeating-conic-gradient(#0f172a 0% 25%, #1e293b 0% 50%) 50% / 20px 20px;
            }
            .light .checkers {
                background: repeating-conic-gradient(#64748b 0% 25%, #cbd5e1 0% 50%) 50% / 20px 20px;
            }

        }

        @media (prefers-color-scheme: light) {
            .checkers {
                background: repeating-conic-gradient(#64748b 0% 25%, #cbd5e1 0% 50%) 50% / 20px 20px;
            }
            .dark .checkers {
                background: repeating-conic-gradient(#0f172a 0% 25%, #1e293b 0% 50%) 50% / 20px 20px;
            }
        }

        :root {
            --star-size: 20px;
            --star-color: #94a3b8;
            --star-background: #1e293b;
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
            background: linear-gradient(90deg, var(--star-background) var(--percent), var(--star-color) var(--percent));
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
</head>
<body class="dark:bg-slate-900 transform duration-200 ease-in-out">
% if get('search', False):
<div x-data="load_search_data()" class="container mx-auto max-w-[1200px] p-5">
% else:
<div class="container mx-auto max-w-[1200px] p-5">
% end
    <div class="grid grid-cols-2 mb-5">
        <div class="col-span-1 grow h-20">
            <a href="/"><img src="/svg/351-dark" alt="351ELEC" class="h-20 hidden dark:block"></a>
            <a href="/"><img src="/svg/351-light" alt="351ELEC" class="h-20 block dark:hidden"></a>
        </div>
        <div class="col-span-1 grid grid-rows-2">
            <div class="self-center flex justify-end justify-self-end items-center space-x-2">
                <span class="text-sm text-slate-800 dark:text-slate-500"><svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
                    </svg></span>
                <label for="toggle" class="w-9 h-5 flex items-center bg-slate-300 rounded-full p-1 cursor-pointer duration-300 ease-in-out dark:bg-slate-600">
                    <div class="toggle-dot bg-white w-4 h-4 rounded-full shadow-md transform duration-300 ease-in-out dark:translate-x-3"></div>
                </label>
                <span class="text-sm text-slate-400 dark:text-white"><svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
                    </svg></span>
                <input id="toggle" type="checkbox" class="hidden" :value="theme" @change="theme = (theme == 'dark' ? 'light' : 'dark')" />
            </div>
            % if get('search', False):
                <input
                    x-ref="searchField"
                    x-model="search"
                    x-on:keydown.window.prevent.slash="$refs.searchField.focus()"
                    placeholder="Search..."
                    type="search"
                    class="self-end justify-self-end w-1/2 flex text-slate-800 placeholder-slate-400 dark:text-slate-300 bg-slate-200 dark:bg-slate-700 dark:bg-slate-700 rounded-lg text-xs font-medium focus:outline-none p-2 px-3"
                />
            % end
        </div>
    </div>

    <div class="text-slate-200 bg-slate-700 dark:bg-slate-700 rounded-lg text-xs font-medium uppercase tracking-wide p-2 px-3 mb-5">
        % for text, href in nav.items():
            <a href="{{ href }}">{{ text }}</a>
            % if list(nav)[-1] != text:
                /
            % end
        % end
    </div>
