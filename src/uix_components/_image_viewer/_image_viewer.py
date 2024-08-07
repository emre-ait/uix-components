import io
from uuid import uuid4
import uix
import os
from PIL import Image
uix.app.add_static_route("seadragon", os.path.dirname(__file__))
uix.html.add_header_item("seadragon", '<script src="/seadragon/openseadragon.min.js"></script>')
uix.html.add_header_item("interactive_seadragon", '<script src="/seadragon/openseadragon-fabricjs-overlay.js"></script>')
uix.html.add_script_source('seadragon', 'seadragon.js',localpath=__file__, beforeMain=False)
icons_path = os.path.join(os.path.dirname(__file__), "icons")


class image_viewer(uix.Element):
    def __init__(self, id = None, value=None, buttonGroup=None, zoom=False, size=(500,500), isInteractive=False):
        super().__init__(id=id, value=value)
        self.tag = "div"
        self.value_name = None

        self.config = {
            "zoom":  zoom,
            "image": value,
        }
        
        if buttonGroup is not None:
            self.config["buttonGroup"] = buttonGroup

        if size is not None and len(size) == 2:
            self.size(*size)

        self.has_PIL_image = False
        self.set_later = True
        self.viewer = "seadragon" if not isInteractive else "interactive-seadragon"

    def init(self):
        self.session.queue_for_send(self.id, self.config, "init-" + self.viewer)
        self.value = self._value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if isinstance(value, Image.Image):
            self.has_PIL_image = True
            self._value = self._create_image_url(value)
        else:
            self.has_PIL_image = False
            self._value = value
            
        if self._value is not None:
            if self.set_later:
                self.session.queue_for_send(self.id, self.value_to_command("open",{"type": "image","url": self._value}), self.viewer)
            else:
                self.session.send(self.id, self.value_to_command("open",{"type": "image","url": self._value}), self.viewer)
            self.set_later = False

    def __del__(self):
        if self.has_PIL_image:
            uix.app.files[self.id] = None

    def _create_image_url(self,img):
        if self.id is None:
            self.id = str(uuid4())
        temp_data = io.BytesIO()
        img.save(temp_data, format="png")
        temp_data.seek(0)
        uix.app.files[self.id] = {"data":temp_data.read(),"type":"image/png"}
        return "/download/"+self.id + "?" + str(uuid4())
    
    def value_to_command(self,command,value):
        return { "action": command, "value": value }


    def zoom_in(self):
        self.session.send(self.id, self.value_to_command("zoomIn", None), "seadragon")

    def zoom_out(self):
        self.session.send(self.id, self.value_to_command("zoomOut", None), "seadragon")

    def home(self):
        self.session.send(self.id, self.value_to_command("home", None), "seadragon")
    
    def fullscreen(self):
        self.session.send(self.id, self.value_to_command("fullscreen", None), "seadragon")
    
    def download(self):
        self.session.send(self.id, self.value_to_command("download", None), "seadragon")

    def open_edit_area(self, value):
        self.session.send(self.id, self.value_to_command("open-edit-area", value), "interactive-seadragon")

    def edit_brush(self, color,opacity, brushSize):
        brushSize = int(brushSize)
        self.session.send(self.id, self.value_to_command("editBrush", {"color": color, "opacity": opacity, "brushSize": brushSize}), "interactive-seadragon")
   

    def set_pan_mode(self):
        self.session.send(self.id, self.value_to_command("setPanMode", None), "interactive-seadragon")

    def eraser_tool(self, brushSize, value=None):
        brushSize = int(brushSize)
        self.session.send(self.id, self.value_to_command("eraserBrush", {"brushSize": brushSize, "isChecked": value}), "interactive-seadragon")

    
