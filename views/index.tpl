% include('_header.tpl', nav={ "Systems": "/" }, search=True)
    <ul role="list" class="grid grid-cols-2 gap-5 sm:gap-6 sm:grid-cols-3 lg:grid-cols-4">
        <template x-for="item in filteredData" :key="item.name">
            <a :href="`/system/${item.folder}`">
                <li class="col-span-1 shadow dark:shadow-none rounded-md" :class="item.roms == 0 ? 'opacity-60' : ''">
                    <div class="flex items-center justify-center w-100 h-20 bg-theme-700 dark:bg-theme-800 text-white text-sm font-medium rounded-t-md">
                        <img loading="lazy" :src="`/svg/${item.name}`" class="w-1/2 max-h-20 p-2" :alt="item.fullname">
                    </div>

                    <div class="flex items-center justify-between border-t border-r border-b border-theme-200 dark:border-theme-900 bg-theme-100 dark:bg-theme-700 rounded-b-md truncate">
                        <div class="flex-1 px-4 py-2 text-sm truncate">
                            <p x-text="item.fullname" class="text-theme-900 font-medium dark:text-theme-200"></p>
                            <p x-show="item.roms > 0" x-text="`${item.roms} ROMs`" class="text-xs text-theme-500 dark:text-theme-400"></p>
                            <p x-show="item.roms == 0" class="text-xs text-theme-400 dark:text-theme-400">No ROMs</p>
                        </div>
                    </div>
                </li>
            </a>
        </template>
    </ul>

    <script>
        let data = {{! systems }};

        function load_search_data() {
            return {
                search: "",
                data: data,
                get filteredData() {
                    if (this.search === "") {
                        return this.data;
                    }
                    return this.data.filter((item) => {
                        return item.fullname.toLowerCase().includes(this.search.toLowerCase())
                            || item.name.toLowerCase().includes(this.search.toLowerCase())
                            || item.folder.toLowerCase().includes(this.search.toLowerCase())
                            || item.manufacturer.toLowerCase().includes(this.search.toLowerCase());
                    });
                },
            };
        }
    </script>
% include('_footer.tpl')
