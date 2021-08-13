/* eslint-disable react/prop-types */
import { merge } from 'lodash';
import { useTheme } from '@material-ui/core/styles';

import ReactApexChart from 'react-apexcharts';
// material
import { Box, Card, CardHeader } from '@material-ui/core';
// utils
import { fNumber } from '../../../utils/formatNumber';
//
import { BaseOptionChart } from '../../charts';

// ----------------------------------------------------------------------

// const CHART_DATA = [{ data: [400, 430, 448, 470, 540, 580, 690, 1100, 1200, 1380] }];

export default function AppConversionRates(props) {
  const theme = useTheme();
  const color = {
    Food: theme.palette.warning.light,
    Clothing: theme.palette.info.light,
    Electronics: theme.palette.primary.light,
    'Healthcare & Wellness': theme.palette.error.light
  };
  const chartOptions = merge(BaseOptionChart(), {
    // eslint-disable-next-line react/prop-types
    colors: [color[props.category]],
    tooltip: {
      marker: { show: false },
      y: {
        formatter: (seriesName) => fNumber(seriesName),
        title: {
          formatter: () => `Orders: `
        }
      }
    },
    plotOptions: {
      bar: { horizontal: true, barHeight: '28%', borderRadius: 2 }
    },
    xaxis: {
      // eslint-disable-next-line react/prop-types
      categories: props.chartData.labels
    }
  });

  function getMonthoverMonthIncrease() {
    const rd = Math.floor(Math.random() * 30 + 1);
    return `(+${rd}%) than last month`;
  }
  return (
    <Card>
      <CardHeader title={props.category} subheader={getMonthoverMonthIncrease()} />
      <Box sx={{ mx: 3 }} dir="ltr">
        <ReactApexChart
          type="bar"
          // eslint-disable-next-line react/prop-types
          series={props.chartData.values}
          options={chartOptions}
          height={364}
        />
      </Box>
    </Card>
  );
}
