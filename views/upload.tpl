<%
include('_header.tpl',
    title=system_name,
    nav=dict(zip(('Systems', system_name, 'Upload'), ('/', '/system/%s' % system, '/upload/%s' % system))),
)
%>
<div class="mt-5 md:mt-0 md:col-span-2">
    <form id="form" action="/upload/{{ system }}" method="POST" enctype="multipart/form-data">
        <div class="shadow dark:shadow-none sm:rounded-md sm:overflow-hidden">
            <div class="px-4 py-5 bg-theme-100 dark:bg-theme-800 sm:p-6 grid grid-cols-6 gap-6">
                <div class="col-span-6" x-data="{ rom_file: false }">
                    <label class="block text-sm font-medium text-theme-700 dark:text-theme-300">ROM File</label>
                    % if get('files', False):
                        % include('_fileupload.tpl', name='rom', extensions=' '.join(extensions), accept=','.join(extensions), existing = files['rom'] if get('files', False) else 'null')
                        <input type="hidden" name="existing_rom" value="{{ game["path"] }}">
                    % else:
                        % include('_fileupload.tpl', name='rom', extensions=' '.join(extensions), accept=','.join(extensions), required=True)
                        <div id="exists" style="display: none;" class="text-sm shadow dark:shadow-none sm:rounded-md bg-rose-500 text-rose-100 p-4 py-2 mt-2">
                            It looks like you're trying to upload a rom that already exists, would you like to <a id="edit-existing" href="#" class="underline font-bold">edit that rom instead</a>?  Please note, duplicate roms will be merged into a single entry.
                        </div>
                        <script>
                            const selectElement = document.querySelector('#rom');
                            selectElement.addEventListener('change', (event) => {
                                const files = event.target.files;
                                const file = files[0];
                                fetch(`/exists/{{ system }}/${file.name}`)
                                    .then(response => response.json())
                                    .then(data => {
                                        console.log(data.exists);
                                        if (data.exists === true) {
                                            document.querySelector('#exists').style.display = 'block';
                                            document.querySelector('#edit-existing').href = `/edit/{{ system }}/${data.as}`;
                                        } else {
                                            // nothing
                                        }
                                    });
                            });
                        </script>
                    % end
                </div>

                <div class="col-span-6">
                    <div class="relative flex items-center">
                        <div class="flex-grow border-t border-theme-400 dark:border-theme-600"></div>
                        <span class="flex-shrink mx-4 text-theme-400 dark:text-theme-600">Optional Metadata</span>
                        <div class="flex-grow border-t border-theme-400 dark:border-theme-600"></div>
                    </div>
                </div>

                <div class="col-span-6">
                    <label for="name" class="block text-sm font-medium text-theme-700 dark:text-theme-300">Name</label>
                    <div class="mt-1 flex">
                        <input type="text" name="name" id="name" class="form-input" placeholder="Battletoads" value="{{ game["name"] if get('game', False) else "" }}">
                    </div>
                </div>

                <div class="col-span-6 sm:col-span-2">
                    <label for="publisher" class="block text-sm font-medium text-theme-700 dark:text-theme-300">Publisher</label>
                    <div class="mt-1 flex">
                        <input type="text" name="publisher" id="publisher" class="form-input" placeholder="Tradewest" value="{{ game["publisher"] if get('game', False) else "" }}">
                    </div>
                </div>

                <div class="col-span-6 sm:col-span-2">
                    <label for="developer" class="block text-sm font-medium text-theme-700 dark:text-theme-300">Developer</label>
                    <div class="mt-1 flex">
                        <input type="text" name="developer" id="developer" class="form-input" placeholder="Rareware" value="{{ game["developer"] if get('game', False) else "" }}">
                    </div>
                </div>

                <div class="col-span-6 sm:col-span-2">
                    <label for="Published" class="block text-sm font-medium text-theme-700 dark:text-theme-300">Published</label>
                    <div class="mt-1 flex">
                        <input type="date" name="Published" id="Published" class="form-input" placeholder="07/13/1991" value="{{ game["releasedate_form"] if get('game', False) else "" }}">
                    </div>
                </div>

                <div class="col-span-6 sm:col-span-2">
                    <label for="genre" class="block text-sm font-medium text-theme-700 dark:text-theme-300">Genre</label>
                    <div class="mt-1 flex">
                        <input type="text" name="genre" id="genre" class="form-input" placeholder="Action, Beat'em Up" value="{{ game["genre"] if get('game', False) else "" }}">
                    </div>
                </div>

                <div class="col-span-6 sm:col-span-1">
                    <label for="players" class="block text-sm font-medium text-theme-700 dark:text-theme-300">Players</label>
                    <div class="mt-1 flex">
                        <input type="text" name="players" id="players" class="form-input" placeholder="2" value="{{ game["players"] if get('game', False) else "" }}">
                    </div>
                </div>

                <div class="col-span-6 sm:col-span-1">
                    <label for="region" class="block text-sm font-medium text-theme-700 dark:text-theme-300">Region</label>
                    <div class="mt-1 flex">
                        <input type="text" name="region" id="region" class="form-input" placeholder="USA" value="{{ game["region"] if get('game', False) else "" }}">
                    </div>
                </div>

                <div class="col-span-6 sm:col-span-2">
                    <label for="rating" class="rating-label block text-sm font-medium text-theme-700 dark:text-theme-300">Rating
                        <input
                          class="rating mt-1.5"
                          max="5"
                          oninput="this.style.setProperty('--value', `${this.valueAsNumber}`)"
                          step="0.25"
                          style="--value:{{ game["rating"] * 5 if get('game', False) else 0 }}"
                          type="range"
                          value="{{ game["rating"] * 5 if get('game', False) else 0 }}">
                      </label>
                </div>

                <div class="col-span-6">
                    <label for="description" class="block text-sm font-medium text-theme-700 dark:text-theme-300">Description</label>
                    <div class="mt-1">
                        <textarea id="description" name="description" rows="3" class="shadow-sm focus:ring-accent-500 dark:focus:ring-accent-400 border-theme-400 focus:border-theme-500 mt-1 block w-full sm:text-sm border text-theme-800 placeholder-theme-400 dark:text-theme-300 bg-theme-200 dark:bg-theme-700 rounded-md">{{ game["desc"] if get('game', False) else "" }}</textarea>
                    </div>
                </div>

                <div class="col-span-6 sm:col-span-3">
                    <label class="block text-sm font-medium text-theme-700 dark:text-theme-300">Marquee</label>
                    % include('_fileupload.tpl', name='marquee', extensions='PNG or JPG files accepted.', accept=".png,.jpg", icon='fa-thin fa-image fa-3x', existing = files['marquee'] if (get('files', False) and 'marquee' in files) else False  )
                </div>

                <div class="col-span-6 sm:col-span-3">
                    <label class="block text-sm font-medium text-theme-700 dark:text-theme-300">Screenshot</label>
                    % include('_fileupload.tpl', name='screenshot', extensions='PNG or JPG files accepted.', accept=".png,.jpg", icon='fa-thin fa-image fa-3x', existing = files['image'] if (get('files', False) and 'image' in files) else False  )
                </div>

                <div class="col-span-6 sm:col-span-3">
                    <label class="block text-sm font-medium text-theme-700 dark:text-theme-300">Box Art</label>
                    % include('_fileupload.tpl', name='boxart', extensions='PNG or JPG files accepted.', accept=".png,.jpg", icon='fa-thin fa-image fa-3x', existing = files['thumbnail'] if (get('files', False) and 'thumbnail' in files) else False  )
                </div>

                <div class="col-span-6 sm:col-span-3">
                    <label class="block text-sm font-medium text-theme-700 dark:text-theme-300">Video</label>
                    % include('_fileupload.tpl', name='video', extensions='MP4 files accepted.', accept=".mp4", icon='fa-thin fa-video fa-3x', existing = files['video'] if (get('files', False) and 'video' in files) else False  )
                </div>
            </div>
            <div class="px-4 py-3 bg-theme-700 text-right sm:px-6">
                <button type="submit" name="submit" id="submit" value="submit" class="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-accent-600 text-accent-100 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-accent-500">Save</button>
            </div>
        </div>
    </form>
</div>

% include('_footer.tpl')
