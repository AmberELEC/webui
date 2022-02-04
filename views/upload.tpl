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
            <div class="px-4 py-5 bg-slate-100 dark:bg-slate-800 sm:p-6 grid grid-cols-4 gap-6">
                <div class="col-span-4">
                    <label class="block text-sm font-medium text-slate-700 dark:text-slate-300">ROM File</label>
                    % include('_fileupload.tpl', name="rom", extensions=" ".join(extensions), accept=",".join(extensions))
                </div>

                <div class="col-span-4">
                    <div class="relative flex items-center">
                        <div class="flex-grow border-t border-slate-400 dark:border-slate-600"></div>
                        <span class="flex-shrink mx-4 text-slate-400 dark:text-slate-600">Optional Metadata</span>
                        <div class="flex-grow border-t border-slate-400 dark:border-slate-600"></div>
                    </div>
                </div>

                <div class="col-span-4">
                    <label for="company-website" class="block text-sm font-medium text-slate-700 dark:text-slate-300">Name</label>
                    <div class="mt-1 flex rounded-md shadow-sm">
                        <input type="text" name="company-website" id="company-website" class="form-input" placeholder="Battletoads">
                    </div>
                </div>

                <div class="col-span-4 sm:col-span-2">
                    <label for="company-website" class="block text-sm font-medium text-slate-700 dark:text-slate-300">Publisher</label>
                    <div class="mt-1 flex rounded-md shadow-sm">
                        <input type="text" name="company-website" id="company-website" class="form-input" placeholder="Tradewest">
                    </div>
                </div>

                <div class="col-span-4 sm:col-span-2">
                    <label for="company-website" class="block text-sm font-medium text-slate-700 dark:text-slate-300">Developer</label>
                    <div class="mt-1 flex rounded-md shadow-sm">
                        <input type="text" name="company-website" id="company-website" class="form-input" placeholder="Rareware">
                    </div>
                </div>

                <div class="col-span-4 sm:col-span-2">
                    <label for="company-website" class="block text-sm font-medium text-slate-700 dark:text-slate-300">Genre</label>
                    <div class="mt-1 flex rounded-md shadow-sm">
                        <input type="text" name="company-website" id="company-website" class="form-input" placeholder="Action, Beat'em Up">
                    </div>
                </div>

                <div class="col-span-4 sm:col-span-1">
                    <label for="company-website" class="block text-sm font-medium text-slate-700 dark:text-slate-300">Players</label>
                    <div class="mt-1 flex rounded-md shadow-sm">
                        <input type="text" name="company-website" id="company-website" class="form-input" placeholder="2">
                    </div>
                </div>

                <div class="col-span-4 sm:col-span-1">
                    <label for="company-website" class="block text-sm font-medium text-slate-700 dark:text-slate-300">Region</label>
                    <div class="mt-1 flex rounded-md shadow-sm">
                        <input type="text" name="company-website" id="company-website" class="form-input" placeholder="USA">
                    </div>
                </div>

                <div class="col-span-4">
                    <label for="about" class="block text-sm font-medium text-slate-700 dark:text-slate-300">Description</label>
                    <div class="mt-1">
                        <textarea id="about" name="about" rows="3" class="shadow-sm focus:ring-emerald-500 dark:focus:ring-emerald-400 border-slate-400 focus:border-slate-500 mt-1 block w-full sm:text-sm border text-slate-800 placeholder-slate-400 dark:text-slate-300 bg-slate-200 dark:bg-slate-700 rounded-md"></textarea>
                    </div>
                </div>

                <div class="col-span-4 sm:col-span-2">
                    <label class="block text-sm font-medium text-slate-700 dark:text-slate-300">Marquee</label>
                    % include('_fileupload.tpl', name='marquee', extensions='PNG or JPG files accepted.', accept=".png,.jpg", icon='fa-thin fa-image fa-3x')
                </div>

                <div class="col-span-4 sm:col-span-2">
                    <label class="block text-sm font-medium text-slate-700 dark:text-slate-300">Screenshot</label>
                    % include('_fileupload.tpl', name='screenshot', extensions='PNG or JPG files accepted.', accept=".png,.jpg", icon='fa-thin fa-image fa-3x')
                </div>

                <div class="col-span-4 sm:col-span-2">
                    <label class="block text-sm font-medium text-slate-700 dark:text-slate-300">Box Art</label>
                    % include('_fileupload.tpl', name='boxart', extensions='PNG or JPG files accepted.', accept=".png,.jpg", icon='fa-thin fa-image fa-3x')
                </div>

                <div class="col-span-4 sm:col-span-2">
                    <label class="block text-sm font-medium text-slate-700 dark:text-slate-300">Video</label>
                    % include('_fileupload.tpl', name='video', extensions='Only MP4 files accepted.', accept=".mp4", icon='fa-thin fa-video fa-3x')
                </div>


            </div>
            <div class="px-4 py-3 bg-slate-700 text-right sm:px-6">
                <button type="submit" class="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-emerald-600 text-emerald-100 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-emerald-500">Save</button>
            </div>
        </div>
    </form>
</div>

% include('_footer.tpl')
