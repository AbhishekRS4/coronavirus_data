import numpy as np
import pandas as pd

from html_utils import HTMLDataParser

class WorldometersHTMLDataParser(HTMLDataParser):
    def __init__(self, url_to_parse):
        super().__init__(url_to_parse)
        self._data_frame = None
        self._data_frame_parsed = None
        self._is_parsed = False

    def preprocess_worldometers_covid_table(self):
        if self._table_rows is not None:
            table_rows = np.array(self._table_rows[1:])
            df_data = pd.DataFrame(table_rows[8:230, :16], columns=self._table_header[:16])
            self._data_frame = df_data
            self._data_frame_parsed = self._data_frame.copy()
        else:
            print("table_rows is none")
        return

    def parse_numeric_data(self, columns_to_exclude=[1, 15]):
        if (self._data_frame_parsed is not None) and (not self._is_parsed):
            columns_to_exclude = set(columns_to_exclude)
            all_columns = set(range(self._data_frame_parsed.shape[1]))

            columns_to_include = list(all_columns - columns_to_exclude)

            for i in range(self._data_frame_parsed.shape[0]):
                for j in columns_to_include:
                    val = self._data_frame_parsed.iloc[i][j]
                    if val == "" or val == "N/A":
                        self._data_frame_parsed.iloc[i][j] = 0
                    else:
                        parsed_val = val.replace("+", "").replace(",", "")
                        try:
                            parsed_val = int(parsed_val)
                        except:
                            parsed_val = int(round(float(parsed_val)))
                        self._data_frame_parsed.iloc[i][j] = parsed_val
            self._is_parsed = True
        else:
            print("data_frame_parsed is none or parse_status is true")
        return

    def calculate_mortality_rate(self):
        if (self._data_frame_parsed is not None) and self._is_parsed:
            mortality_rate = 100 * self._data_frame_parsed.TotalDeaths.to_numpy() \
                / self._data_frame_parsed.TotalCases.to_numpy()
            mortality_rate = mortality_rate.astype(np.float32)
            self._data_frame_parsed["MortalityRate"] = np.around(mortality_rate, decimals=4)
        else:
            print("data_frame_parsed is none or parse_status is false")
        return
