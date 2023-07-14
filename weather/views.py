from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from htmx.views import HTMXMixin
from plotly import express as px
import pandas as pd

from .models import Data
# Create your views here.


def _concat_dataframe(df: pd.DataFrame, labels, goal_column_name):
    out = []
    for label in labels:
        temp = df[['date', label]]
        print(temp.columns)
        temp = temp.rename({label: goal_column_name}, axis='columns')
        temp['type'] = label
        out.append(temp)
    return pd.concat(out)


class IndexView(LoginRequiredMixin, HTMXMixin, TemplateView):
    template_name = 'weather/index.html'

    def get_from_date(self):
        if 'from_date' in self.request.GET:
            ...  # parsing input date
        return timezone.now()-timezone.timedelta(days=7)

    def get_to_date(self):
        if 'to_date' in self.request.GET:
            ...  # parsing input date
        return timezone.now()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        to_date = self.get_to_date()
        from_data = self.get_from_date()
        df = pd.DataFrame(
            Data.objects.filter(date__gte=from_data, date__lte=to_date).values(
                'date', 'temperature', 'temperature_dome', 'dewpoint',
                'humidity', 'humidity_dome'
            )
        )
        if len(df) == 0:
            return context

        temperatures = _concat_dataframe(df, ['temperature', 'temperature_dome', 'dewpoint'], 'C')

        humidity = _concat_dataframe(df, ['humidity', 'humidity_dome'], 'humidity')
        temperature_fig = px.line(temperatures, 'date', 'C', color='type')

        # temperature_fig.data[0].update(mode='markers+lines')
        [d.update(mode='markers+lines') for d in temperature_fig.data]
        temperature_fig.update_layout(
            {
                'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                'paper_bgcolor': 'rgba(0, 0, 0, 0)',
                'font_color': 'rgba(220, 220, 220, 0.8)'
            }
        )
        context['graph'] = {
            'temperature': temperature_fig.to_json()
        }
        return context
