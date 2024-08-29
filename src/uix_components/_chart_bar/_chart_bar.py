import uix
from uix import Element
from uix.elements import canvas
from uix_components._chart_bar.chart_utils import ChartUtils

uix.app.serve_module_static_files(__file__)

script = """
    event_handlers["init-chart"] = function (id, value, event_name) {
        Chart.register(ChartDataLabels);
        let chart = new Chart(id, value);
        elm = document.getElementById(id);
        elm.chart = chart;
    };
"""
def register_resources(cls):
    cls.register_script("chart-js-umd", "/_chart_bar/chart.umd.js", is_url=True)
    cls.register_script("chartjs-plugin-datalabels", "/_chart_bar/chartjs-plugin-datalabels.min.js", is_url=True)
    cls.register_script("chart-js", script)
    return cls

@register_resources
class chart_bar(Element):
    def __init__(self, id, value=None, labels=None, options=None):
        super().__init__(id=id, value=value)
        self._value = value
        self.value_name = None
        self.labels = labels
        self.options = options
        self.canvas_id = id+"_canvas"

        self.chartData ={
            "type": "bar",
            "data": {
                "labels": [],

                "datasets": [
                ],
            },
            "plugins": ["ChartDataLabels"],
            "options": {
                "responsive": None,
                "plugins": {
                    "legend": {
                        "position": None,
                    },
                    "title": {
                        "display": None,
                        "text": None
                    },
                    "datalabels": {
                        "display": True,
                        "color": "white",
                        "font": {
                            "size": 20,
                            "weight": "bold"
                        },
                    }
                }
            },
           

        }

        ChartUtils.dataset_importer(self.chartData, self.value, self.labels)
        ChartUtils.set_options(self.chartData, self.options)

        with self:
            self.canvas = canvas(id=self.canvas_id, value=self.chartData)

    def init(self):
        self.session.queue_for_send(self.canvas_id, self.canvas.value, "init-chart")

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        ChartUtils.dataset_importer(self.chartData, value, self.labels)
        ChartUtils.set_options(self.chartData, self.options)
        with self:
            self.canvas = canvas(id=self.canvas_id,value = self.chartData)
        self.init()
        self.update()
