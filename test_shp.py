import geopandas as gpd
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq



gpd = pd.read_parquet('notificacoes_count.parquet')

print(gpd.head().to_json())
