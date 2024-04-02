import flet
import librec


class TextEntry(flet.UserControl):
    def __init__(self, label: str, *w, text_type: str=None, value=None, custom_filter: str=None, **kw):
        super(TextEntry, self).__init__(*w, **kw)
        self.label = label
        self.value = value
        self.text_type = text_type
        self.custom_filter = custom_filter


    def build(self):
        match (self.text_type):
            case 'text':
                input_filter = '^[a-zA-Z]*' # only char's
            case 'number':
                input_filter = '^[0-9]*'
            case 'alpha':
                input_filter = '^[0-9a-zA-Z]*' # alphanumeric
            case 'custom':
                input_filter = self.custom_filter
            case _:
                input_filter = None
        return flet.TextField(label=self.label, value=self.value, expand=True, input_filter=flet.InputFilter(input_filter))


class OptionList(flet.UserControl):
    def __init__(self, label: str, options: list, value: str, *w, **kw):
        super(OptionList,self).__init__(*w, **kw)
        self.label = label
        self.options = options
        self.value = value

    def build(self):
        return flet.Dropdown(label=self.label, options=[flet.dropdown.Option(opt) for opt in self.options], value=self.value)


class CheckLists(flet.UserControl):
    def __init__(self, *w, _dict: dict, **kw):
        super(CheckLists, self).__init__(*w, **kw)
        self._dict = _dict # {label:value}

    def build(self):
        return flet.Row(controls=[
                flet.Checkbox(label=label, value=value) for label, value in self._dict.items()
            ])


class Audio(flet.UserControl):
    def __init__(self, *w, **kw):
        super(Audio, self).__init__(*w, **kw)
        self.audio_bitrate = TextEntry(label='audio bitrate (suffix: K, M):', value='128K', text_type='custom', custom_filter=r'^[0-9]+[KMkm]*')
        self.audio_buffer = TextEntry(label='audio buffer (milliseconds):', text_type='number', value='50')
        self.audio_codec_name = OptionList(label='audio codec name:', options=('opus', 'aac', 'flac', 'raw'), value='opus')
        self.audio_codec_options = TextEntry(label='audio codec options:', text_type='custom', custom_filter=r'^([A-Z_]+)\:(int|long|float|string)\=([A-Za-z0-9]+)', value='')
        self.audio_encoder_name = OptionList(label='audio encoder name:', options=('get', 'from', '--list-encoders'), value='get')
        self.audio_source = OptionList(label='audio source:', options=('output', 'mic'), value='output')
        self.audio_output_buffer = TextEntry(label='audio output buffer (milliseconds):', text_type='number', value='5')
        self.audio_disable = CheckLists(_dict={'no audio': False, 'no audio playback': False, 'require audio': True})

    def build(self):
        return flet.Container(content=flet.Column(controls=[
                                self.audio_bitrate,
                                self.audio_buffer,
                                self.audio_codec_name,
                                self.audio_codec_options,
                                self.audio_encoder_name,
                                self.audio_source,
                                self.audio_output_buffer,
                                self.audio_disable,
                            ]), border=flet.border.all(3,flet.colors.BLUE), border_radius=flet.border_radius.all(10),padding=10,)

class Video(flet.UserControl):
    def __init__(self, *w, **kw):
        super(Video, self).__init__(*w, **kw)
        self.video_bitrate = TextEntry(label='video bitrate (suffix: K, M):', value='8M', text_type='custom', custom_filter=r'^[0-9]+[KMkm]*')
        self.video_codec_name = OptionList(label='video codec name:', options=('h264', 'h265', 'av1'), value='h264')
        self.video_codec_options = TextEntry(label='video codec options:', text_type='custom', custom_filter=r'^([A-Z_]+)\:(int|long|float|string)\=([A-Za-z0-9]+)', value='')
        self.video_encoder_name = OptionList(label='video encoder name:', options=('get', 'from', '--list-encoders'), value='get')
        self.video_source = OptionList(label='video source:', options=('display', 'camera'), value='display')
        self.video_disable = CheckLists(_dict={'no video': False, 'no video playback': False, 'require video': True})
        self.video_max_size = TextEntry(label='video max size:', value='0', text_type='number')
        self.video_max_fps = TextEntry(label='video max fps:', value='', text_type='number')


    def build(self):
        return flet.Container(content=flet.Column(controls=[
                                self.video_bitrate,
                                self.video_codec_name,
                                self.video_codec_options,
                                self.video_encoder_name,
                                self.video_source,
                                self.video_max_size,
                                self.video_disable,
                            ]), border=flet.border.all(3,flet.colors.BLUE), border_radius=flet.border_radius.all(10),padding=10,)



class Display(flet.UserControl):
    def __init__(self, *w, **kw):
        super(Display, self).__init__(*w, **kw)
        self.display_buffer = TextEntry(label='display buffer (milliseconds):', value='0', text_type='number')
        self.display_id = OptionList(label='display id:', value='0', options=('get', 'from', '--list-displays'))
        self.display_orientation = OptionList(label='display orientation:', value='0', options='0 90 180 270 flip0 flip90 flip180 flip270'.split(' '))

    def build(self):
        return flet.Container(content=flet.Column(controls=[
                self.display_buffer,
                self.display_id,
                self.display_orientation,
            ]), border=flet.border.all(3,flet.colors.BLUE), border_radius=flet.border_radius.all(10),padding=10,)


class Window(flet.UserControl):
    def __init__(self, *w, **kw):
        super(Window, self).__init__(*w, **kw)
        self.window_title = TextEntry(label='window title:',text_type='alphanumeric', value='DroidRec')
        self.window_x = TextEntry(label='window x:', value='auto', text_type='custom', custom_filter=r'^(auto|[0-9]+)$')
        self.window_y = TextEntry(label='window y:', value='auto', text_type='custom', custom_filter=r'^(auto|[0-9]+)$')
        self.window_width = TextEntry(label='window width (0 = auto):', value='0', text_type='number')
        self.window_height = TextEntry(label='window height (0 = auto):', value='0', text_type='number')
        self.window_options = CheckLists(_dict={'window borderless': False, 'always on top': False, 'fullscreen': False})
        self.window_render_driver = OptionList(label='render driver:', value='opengles2',options=("direct3d", "opengl", "opengles2", "opengles", "metal", "software"))

        
    def build(self):
        return flet.Container(content=flet.Column(controls=[
                self.window_title,
                self.window_x,
                self.window_y,
                self.window_width,
                self.window_height,
                self.window_options,
            ]), border=flet.border.all(3,flet.colors.BLUE), border_radius=flet.border_radius.all(10),padding=10,)


class V4L2(flet.UserControl):
    def __init__(self, *w, **kw):
        super(V4L2, self).__init__(*w, **kw)
        self.v4l2_sink = TextEntry(label='v4l2 sink (/dev/videoN):', value='')
        self.v4l2_buffer = TextEntry(label='v4l2 buffer(milliseconds):', value='0', text_type='number')

    def build(self):
        return flet.Container(content=flet.Column(controls=[
                self.v4l2_sink,
                self.v4l2_buffer,

            ]), border=flet.border.all(3,flet.colors.BLUE), border_radius=flet.border_radius.all(10),padding=10,)


class Record(flet.UserControl):
    def __init__(self, *w, **kw):
        super(Record, self).__init__(*w, **kw)
        self.record_directory = TextEntry(label='record directory:', value='~/Videos')
        self.record_filename = TextEntry(label='record filename:', value='{package}_{date}_{time}.{ext}')
        self.record_format = OptionList(label='record format:', value='mkv', options=('mp4','mkv','m4a','mka','opus','aac','flac','wav'))
        self.record_orientation = OptionList(label='record orientation:', value='0', options=('0','90','180','270'))

        
    def build(self):
        return flet.Container(content=flet.Column(controls=[
                self.record_directory,
                self.record_filename,
                self.record_format,
                self.record_orientation,

            ]), border=flet.border.all(3,flet.colors.BLUE), border_radius=flet.border_radius.all(10),padding=10,)


class Input(flet.UserControl):
    def __init__(self, *w, **kw):
        super(Input, self).__init__(*w, **kw)
        self.options = CheckLists(_dict={'otg': False, 'no keyboard': True, 'no mouse': True})
        self.keyboard_mode = OptionList(label='keyboard mode', options=("disabled", "sdk", "uhid", "aoa"), value='uhid')
        self.mouse_mode = OptionList(label='mouse mode', options=("disabled", "sdk", "uhid", "aoa"), value='uhid')


    def build(self):
        return flet.Container(content=flet.Column(controls=[
                self.options,
                self.keyboard_mode,
                self.mouse_mode

            ]), border=flet.border.all(3,flet.colors.BLUE), border_radius=flet.border_radius.all(10),padding=10,)



class Other(flet.UserControl):
    def __init__(self, *w, **kw):
        super(Other, self).__init__(*w, **kw)
        self.pause_on_exit = OptionList(label='pause on exit:', value='false', options=('true','false','if-error'))
        self.check_buttons = CheckLists(_dict={'stay awake': False, 'version': False,'turn screen off': False, 'otg': False,'no control': True})
        self.verbosity = OptionList(label='verbosity:',value='info', options=('verbose','debug','info','warn','error'))
        
    def build(self):
        return flet.Container(content=flet.Column(controls=[
                self.pause_on_exit,
                self.check_buttons,
                self.verbosity

            ]), border=flet.border.all(3,flet.colors.BLUE), border_radius=flet.border_radius.all(10),padding=10,)


class App:
    def __init__(self, title: str='droidrec', width: int=None, height: int=None):
        self.title = title
        self.width = width
        self.height = height
        self.page = None

    def main(self, page: flet.Page):
        self.page = page
        if self.page.platform not in ('android', 'ios'):
            self.page.title = self.title
            self.page.window_max_width = self.width
            self.page.window_max_height = self.height
        self.page.update()
        self.__build_ui()

    def __build_ui(self):
        self.audio = flet.Tab(text='audio', content=Audio(), icon=flet.icons.AUDIO_FILE)
        self.video = flet.Tab(text='video', content=Video(), icon=flet.icons.VIDEO_FILE)
        self.display = flet.Tab(text='display', content=Display(), icon=flet.icons.DISPLAY_SETTINGS)
        self.record = flet.Tab(text='record', content=Record(), icon=flet.icons.CAMERA)
        self.window = flet.Tab(text='window', content=Window(), icon=flet.icons.WINDOW)
        self.v4l2 = flet.Tab(text='v4l2', content=V4L2(), icon=flet.icons.VIDEOCAM)
        self.input = flet.Tab(text='input', content=Input(), icon=flet.icons.KEYBOARD)
        self.other = flet.Tab(text='other', content=Other(), icon=flet.icons.SETTINGS)

        self.home = flet.Tabs(tabs=[self.audio, self.video, self.display, self.record, self.window, self.v4l2, self.input, self.other])

        self.page.controls.append(flet.SafeArea(content=self.home, expand=True))
        self.page.update()


if __name__ == '__main__':
    app = App(width=800, height=600)
    flet.app(target=app.main)
