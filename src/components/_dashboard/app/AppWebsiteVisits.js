import { merge } from 'lodash';
import ReactApexChart from 'react-apexcharts';
// material
import { Card, CardHeader, Box } from '@material-ui/core';
import { useTheme } from '@material-ui/core/styles';

import { BaseOptionChart } from '../../charts';

// ----------------------------------------------------------------------

const CHART_DATA = [
  {
    name: 'Food',
    type: 'area',
    data: [75, 65, 71, 62, 98, 100, 49, 45]
  },
  {
    name: 'Clothing',
    type: 'line',
    data: [44, 41, 67, 43, 21, 41, 56, 43]
  },
  {
    name: 'Electronics',
    type: 'line',
    data: [16, 36, 30, 45, 35, 64, 52, 36]
  },
  {
    name: 'Health & Wellness',
    type: 'line',
    data: [25, 36, 45, 35, 52, 59, 36, 39]
  }
];

export default function AppWebsiteVisits() {
  const theme = useTheme();
  const chartOptions = merge(BaseOptionChart(), {
    colors: [
      theme.palette.warning.lighter,
      theme.palette.info.main,
      theme.palette.primary.main,
      theme.palette.error.main
    ],
    stroke: { width: [0, 2, 3] },
    plotOptions: { bar: { columnWidth: '11%', borderRadius: 4 } },
    fill: { type: ['solid', 'solid', 'solid', 'solid'] },
    labels: [
      '01/01/2021',
      '02/01/2021',
      '03/01/2021',
      '04/01/2021',
      '05/01/2021',
      '06/01/2021',
      '07/01/2021',
      '08/01/2021'
    ],
    xaxis: { type: 'datetime' },
    tooltip: {
      shared: true,
      intersect: false,
      y: {
        formatter: (y) => {
          if (typeof y !== 'undefined') {
            return `${y.toFixed(0)} visits`;
          }
          return y;
        }
      }
    }
  });

  return (
    <Card>
      <CardHeader title="Monthly Expense Trends" subheader="(+43%) than last year" />
      <Box sx={{ p: 3, pb: 1 }} dir="ltr">
        <ReactApexChart type="line" series={CHART_DATA} options={chartOptions} height={364} />
      </Box>
    </Card>
  );
}
