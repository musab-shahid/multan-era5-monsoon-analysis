import unittest,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
import pandas as pd
import numpy as np
from reproduce_monsoon import aggregate_days,longest_dry

class TimingTests(unittest.TestCase):
 def frame(self,times,values=None):
  return pd.DataFrame({'utc':pd.to_datetime(times),'precip_mm':values if values is not None else np.ones(len(times)),'temp_c':np.full(len(times),30.)})
 def test_midnight_rain_belongs_to_previous_day_temperature_does_not(self):
  d=aggregate_days(self.frame(['2020-08-31 19:00'],[7.]))
  self.assertEqual(d.loc['2020-08-31','observed_rain_mm'],7.)
  self.assertEqual(d.loc['2020-09-01','temp_hours'],1)
 def test_complete_local_rain_day_has_24_intervals(self):
  d=aggregate_days(self.frame(pd.date_range('2020-08-30 20:00',periods=24,freq='h')))
  self.assertEqual(d.loc['2020-08-31','precip_mm'],24.)
 def test_missing_hour_is_not_a_zero_rainfall_measurement(self):
  times=pd.date_range('2020-08-30 20:00',periods=24,freq='h').delete(8)
  d=aggregate_days(self.frame(times));self.assertTrue(pd.isna(d.loc['2020-08-31','precip_mm']))
  self.assertEqual(d.loc['2020-08-31','rain_hours'],23)
 def test_no_fake_dates_between_seasons(self):
  d=aggregate_days(self.frame(['2019-06-02 12:00','2020-06-02 12:00']))
  self.assertEqual(len(d),2)
 def test_missing_day_breaks_dry_spell(self):
  self.assertEqual(longest_dry([0.,0.,np.nan,0.,0.,0.]),3)
 def test_utc_and_pkt_date_windows_differ(self):
  h=self.frame(['2020-08-31 22:00'],[4.])
  self.assertEqual(aggregate_days(h,0).loc['2020-08-31','observed_rain_mm'],4.)
  self.assertEqual(aggregate_days(h,5).loc['2020-09-01','observed_rain_mm'],4.)

if __name__=='__main__':unittest.main()
