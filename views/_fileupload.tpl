<div x-data="{ files: null }" id="file_upload_{{ name }}" class="mt-1 block w-full px-6 pt-5 pb-6 relative border border-slate-400 dark:border-slate-500 text-slate-800 placeholder-slate-400 dark:text-slate-300 bg-slate-200 dark:bg-slate-700 border-dashed rounded-md">
    <input type="file" name="{{ name }}"
            class="absolute inset-0 z-50 m-0 p-0 w-full h-full outline-none opacity-0 cursor-pointer"
            accept={{accept}}
            x-on:change="files = $event.target.files; console.log($event.target.files);"
            x-on:dragover="$el.classList.add('active')" x-on:dragleave="$el.classList.remove('active')" x-on:drop="$el.classList.remove('active')"
    >
    <template x-if="files !== null">
        <div class="flex flex-col space-y-1">
            <template x-for="(_,index) in Array.from({ length: files.length })">
                <div class="flex flex-row items-center space-x-2">
                    <template x-if="files[index].type.includes('application/')"><i class="self-center far fa-file-alt fa-fw"></i></template>
                    <template x-if="files[index].type.includes('image/')"><i class="self-center far fa-file-image fa-fw"></i></template>
                    <template x-if="files[index].type.includes('video/')"><i class="self-center far fa-file-video fa-fw"></i></template>
                    <div class="font-medium grow text-slate-600 dark:text-slate-300 self-center" x-text="files[index].name">Uploading</div>
                    <div class="text-xs self-end text-slate-500 self-center" x-text="filesize(files[index].size)">...</div>
                </div>
            </template>
        </div>
    </template>
    <template x-if="files === null">
        <div class="flex flex-col space-y-2 items-center justify-center flex text-sm text-slate-600 dark:text-slate-300 space-y-1">
            <i class="{{ get('icon', False) or 'fa-thin fa-upload fa-3x' }}"></i>
            <div><span class="text-emerald-500">Upload a file</span> or drag and drop.</div>
            <div class="text-xs text-slate-500">{{ extensions }}</div>
        </div>
    </template>
</div>
