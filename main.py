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
    def __init__(self, label: str, options: list, default: str, *w, **kw):
        super(OptionList,self).__init__(*w, **kw)
        self.label = label
        self.options = options
        self.default = default

    def build(self):
        return flet.Dropdown(label=self.label, options=[flet.dropdown.Option(opt) for opt in self.options], value=self.default)


class CheckLists(flet.UserControl):
    def __init__(self, *w, _dict: dict, **kw):
        super(CheckLists, self).__init__(*w, **kw)
        self._dict = _dict # {label:value}

    def build(self):
        return flet.Row(controls=[
                flet.Checkbox(label=label+":", value=value) for label, value in self._dict.items()
            ])


class Audio(flet.UserControl):
    def __init__(self, *w, **kw):
        super(Audio, self).__init__(*w, **kw)
        self.audio_bitrate = TextEntry(label='audio bitrate (suffix: K, M):', value='128K', text_type='custom', custom_filter=r'^[0-9]+[KMkm]*')
        self.audio_buffer = TextEntry(label='audio buffer (milliseconds):', text_type='number', value='50')
        self.audio_codec_name = OptionList(label='audio codec name:', options=('opus', 'aac', 'flac', 'raw'), default='opus')
        self.audio_codec_options = TextEntry(label='audio codec options:', text_type='custom', custom_filter=r'^([A-Z_]+)\:(int|long|float|string)\=([A-Za-z0-9]+)', value='')
        self.audio_encoder_name = OptionList(label='audio encoder name:', options=('get', 'from', '--list-encoders'), default='get')
        self.audio_source = OptionList(label='audio source:', options=('output', 'mic'), default='output')
        self.audio_output_buffer = TextEntry(label='audio output buffer (milliseconds):', text_type='number', value='5')
        self.audio_disable = CheckLists(_dict={'no audio': False, 'no audio playback': False, 'require audio': False})

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
        self.audio = Audio()

        self.home = flet.Column(controls=[self.audio])

        self.page.controls.append(flet.SafeArea(content=self.home, expand=True))
        self.page.update()

if __name__ == '__main__':
    app = App()
    flet.app(target=app.main)
