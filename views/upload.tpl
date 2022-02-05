<%
include('_header.tpl',
    title=system_name,
    actions={ 'Upload ROM': '/upload/%s' % system },
    nav=dict(zip(('Systems', system_name, 'Upload'), ('/', '/system/%s' % system, '/upload/%s' % system))),
)
%>
<div class="mt-5 md:mt-0 md:col-span-2">
    <form action="#" method="POST">
        <div class="shadow dark:shadow-none sm:rounded-md sm:overflow-hidden">
            <div class="px-4 py-5 bg-theme-100 dark:bg-theme-800 sm:p-6 grid grid-cols-4 gap-6">
                <div class="col-span-4">
                    <label class="block text-sm font-medium text-theme-700 dark:text-theme-300">ROM File</label>
                    % include('_fileupload.tpl', name="rom", extensions=" ".join(extensions), accept=",".join(extensions))
                </div>

                <div class="col-span-4">
                    <div class="relative flex items-center">
                        <div class="flex-grow border-t border-theme-400 dark:border-theme-600"></div>
                        <span class="flex-shrink mx-4 text-theme-400 dark:text-theme-600">Optional Metadata</span>
                        <div class="flex-grow border-t border-theme-400 dark:border-theme-600"></div>
                    </div>
                </div>

                <div class="col-span-4">
                    <label for="company-website" class="block text-sm font-medium text-theme-700 dark:text-theme-300">Name</label>
                    <div class="mt-1 flex rounded-md shadow-sm">
                        <input type="text" name="company-website" id="company-website" class="form-input" placeholder="Battletoads">
                    </div>
                </div>

                <div class="col-span-4 sm:col-span-2">
                    <label for="company-website" class="block text-sm font-medium text-theme-700 dark:text-theme-300">Publisher</label>
                    <div class="mt-1 flex rounded-md shadow-sm">
                        <input type="text" name="company-website" id="company-website" class="form-input" placeholder="Tradewest">
                    </div>
                </div>

                <div class="col-span-4 sm:col-span-2">
                    <label for="company-website" class="block text-sm font-medium text-theme-700 dark:text-theme-300">Developer</label>
                    <div class="mt-1 flex rounded-md shadow-sm">
                        <input type="text" name="company-website" id="company-website" class="form-input" placeholder="Rareware">
                    </div>
                </div>

                <div class="col-span-4 sm:col-span-2">
                    <label for="company-website" class="block text-sm font-medium text-theme-700 dark:text-theme-300">Genre</label>
                    <div class="mt-1 flex rounded-md shadow-sm">
                        <input type="text" name="company-website" id="company-website" class="form-input" placeholder="Action, Beat'em Up">
                    </div>
                </div>

                <div class="col-span-4 sm:col-span-1">
                    <label for="company-website" class="block text-sm font-medium text-theme-700 dark:text-theme-300">Players</label>
                    <div class="mt-1 flex rounded-md shadow-sm">
                        <input type="text" name="company-website" id="company-website" class="form-input" placeholder="2">
                    </div>
                </div>

                <div class="col-span-4 sm:col-span-1">
                    <label for="company-website" class="block text-sm font-medium text-theme-700 dark:text-theme-300">Region</label>
                    <div class="mt-1 flex rounded-md shadow-sm">
                        <input type="text" name="company-website" id="company-website" class="form-input" placeholder="USA">
                    </div>
                </div>

                <div class="col-span-4">
                    <label for="about" class="block text-sm font-medium text-theme-700 dark:text-theme-300">Description</label>
                    <div class="mt-1">
                        <textarea id="about" name="about" rows="3" class="shadow-sm focus:ring-emerald-500 dark:focus:ring-emerald-400 border-theme-400 focus:border-theme-500 mt-1 block w-full sm:text-sm border text-theme-800 placeholder-theme-400 dark:text-theme-300 bg-theme-200 dark:bg-theme-700 rounded-md"></textarea>
                    </div>
                </div>

                <div class="col-span-4 sm:col-span-2">
                    <label class="block text-sm font-medium text-theme-700 dark:text-theme-300">Marquee</label>
                    % include('_fileupload.tpl', name='marquee', extensions='PNG or JPG files accepted.', accept=".png,.jpg", icon='fa-thin fa-image fa-3x')
                </div>

                <div class="col-span-4 sm:col-span-2">
                    <label class="block text-sm font-medium text-theme-700 dark:text-theme-300">Screenshot</label>
                    % include('_fileupload.tpl', name='screenshot', extensions='PNG or JPG files accepted.', accept=".png,.jpg", icon='fa-thin fa-image fa-3x')
                </div>

                <div class="col-span-4 sm:col-span-2">
                    <label class="block text-sm font-medium text-theme-700 dark:text-theme-300">Box Art</label>
                    % include('_fileupload.tpl', name='boxart', extensions='PNG or JPG files accepted.', accept=".png,.jpg", icon='fa-thin fa-image fa-3x')
                </div>

                <div class="col-span-4 sm:col-span-2">
                    <label class="block text-sm font-medium text-theme-700 dark:text-theme-300">Video</label>
                    % include('_fileupload.tpl', name='video', extensions='Only MP4 files accepted.', accept=".mp4", icon='fa-thin fa-video fa-3x')
                </div>


            </div>
            <div class="px-4 py-3 bg-theme-700 text-right sm:px-6">
                <button type="submit" class="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-emerald-600 text-emerald-100 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-emerald-500">Save</button>
            </div>
        </div>
    </form>
</div>

% include('_footer.tpl')
