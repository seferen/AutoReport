from influxdb import DataFrameClient
import pandas as pd
import plotly.graph_objects as go
import plotly.offline as off
from datetime import datetime

TIMEFORMAT = '%Y-%m-%d %H:%M'


class Grafics():

    def __init__(self, table: str,
                 dateFrom: str = "1970-01-01 00:00",
                 dateTo: str = datetime.now().strftime(TIMEFORMAT),
                 host: str = 'localhost',
                 port: int = 8086,
                 db='myDb',
                 graficName: str = ""):
        self.table = table
        self.dateFrom = dateFrom
        self.dateTo = dateTo
        self.host = host
        self.port = port
        self.db = db
        self.graficName = graficName
        pass

    # получаем датафрейм из InfluxDb
    def get_data_frame_InfluxDb(self
                                ) -> pd.DataFrame:
        select = 'SELECT * FROM "{}" WHERE time >= {}000000000 AND time <= {}000000000'.format(
            self.table,
            datetime.strptime(self.dateFrom, TIMEFORMAT).strftime('%s'),
            datetime.strptime(self.dateTo, TIMEFORMAT).strftime('%s')
        )

        client = DataFrameClient(host=self.host, port=self.port, database=self.db)

        result = client.query(select, chunked=True)

        column = next(iter(result))

        data: pd.DataFrame = result[column]

        data.index = data.index.tz_convert('Europe/Moscow')

        data.index = data.index.tz_localize(None)

        return data

    # собираем график
    def get_figure_str(self, data: pd.DataFrame, charts: dict, tags: dict) -> str:
        fig: go.Figure = go.Figure()
        hosts = data['host'].unique()

        for tag in tags:
            data = data[data[tag] == tags[tag]]

        print(data)

        for host in hosts:
            graf = data[data['host'] == host]
            for i in charts:
                print('Avalyble columns: ' + ', '.join(list(graf.columns)))
                fig.add_trace(go.Scatter(y=graf[i], name='{}: {}'.format(host, charts[i])))

        fig.update_layout(
            title=self.graficName,
            showlegend=True,
            legend_orientation='h'
        )

        return off.plot(fig, output_type='div', auto_open=False)


if __name__ == '__main__':

    a = [Grafics('cpu', '2020-01-03 12:00', '2020-01-03 13:00', graficName="Утилизация CPU"),
         Grafics('cpu', '2020-01-03 12:00', '2020-01-03 13:00')]
    result = []

    for t in a:
        data = t.get_data_frame_InfluxDb()
        result.append(t.get_figure_str(data, {'usage_idle': 'cpu'}, {'cpu': 'cpu-total'}))

    # собираем html
    with open("test.html", 'w') as f:
        f.write("\n".join(result))
