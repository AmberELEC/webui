<%
include('_header.tpl',
    title=system_name,
    search=True,
    actions={ 'Upload ROM': '/upload/%s' % system },
    nav=dict(zip(('Systems', system_name), ('/', '/system/%s' % system))),
)
%>
    <ul role="list" class="mt-3 grid grid-cols-2 gap-5 sm:gap-6 sm:grid-cols-3 lg:grid-cols-4">
        <!-- <li class="col-span-1 shadow dark:shadow-none rounded-md">
            <div class="flex items-center justify-center w-100 h-20 bg-emerald-600 dark:bg-emerald-700 text-white text-sm font-medium rounded-t-md">
                <img loading="lazy" src="/svg/{{ system_info["name" ]}}" class="w-1/2 max-h-20 p-2" :alt="item.fullname">
            </div>
            <div class="flex items-center justify-between border-t border-r border-b border-transparent bg-slate-100 dark:bg-emerald-600 rounded-b-md truncate">
                <div class="flex-1 px-4 py-2 text-sm truncate">
                    <p class="text-emerald-700 font-medium dark:text-emerald-200">{{ system_info["manufacturer"] }} / {{ system_info["fullname"] }}</p>
                    <p class="text-xs text-emerald-500 dark:text-emerald-200 dark:text-emerald-300">Released {{ system_info["release"] }}</p>
                </div>
            </div>
        </li> -->
        <template x-for="item in filteredData" :key="item.path">
            <a :href="`/system/{{ system }}/${item.id || item.path}`">
                <li class="col-span-1 shadow dark:shadow-none rounded-md">
                    <div class="flex items-center justify-center w-100 h-20 bg-slate-700 dark:bg-slate-800 text-white text-sm font-medium rounded-t-md">
                        <img x-show="item.marquee" loading="lazy" :src="`/image/{{ system }}/${item.marquee}`" class="w-1/2 max-h-20 p-2" :alt="item.name">
                        <img x-show="!item.marquee && item.image" loading="lazy" :src="`/image/{{ system }}/${item.image}`" class="w-1/2 max-h-20 p-2" :alt="item.name">
                        <img x-show="!item.marquee && !item.image" loading="lazy" src="/svg/{{ system }}" class="w-1/2 max-h-20 p-2" :alt="item.name">
                    </div>
                    <div class="flex items-center justify-between border-t border-r border-b border-slate-200 dark:border-slate-900 bg-slate-100 dark:bg-slate-700 rounded-b-md truncate">
                        <div class="flex-1 px-4 py-2 text-sm truncate">
                            <p x-text="item.name" class="text-slate-900 font-medium dark:text-slate-200"></p>
                            <p x-text="item.path" class="text-xs text-slate-500 dark:text-slate-200 dark:text-slate-400"></p>
                        </div>
                    </div>
                </li>
            </a>
        </template>
    </ul>

    <script>
        let data = {{! games }};

        function load_search_data() {
            return {
                search: "",
                data: data,
                get filteredData() {
                    if (this.search === "") {
                        return this.data;
                    }
                    return this.data.filter((item) => {
                        return item.name.toLowerCase().includes(this.search.toLowerCase())
                            || item.path.toLowerCase().includes(this.search.toLowerCase());
                    });
                },
            };
        }
    </script>
% include('_footer.tpl')
