// material
import { Box, Grid, Container, Typography } from '@material-ui/core';
// components
import Page from '../components/Page';
import {
  AppNewUsers,
  AppBugReports,
  AppItemOrders,
  AppWeeklySales,
  AppOrderTimeline,
  AppCurrentVisits,
  AppWebsiteVisits,
  AppConversionRates
} from '../components/_dashboard/app';
import FoodData from '../_mocks_/Food';
import ClothingData from '../_mocks_/Clothing';
import ElectronicsData from '../_mocks_/Electronics';
import HealthcareData from '../_mocks_/H&W';

// ----------------------------------------------------------------------

export default function DashboardApp() {
  return (
    <Page title="Dashboard">
      <Container maxWidth="xl">
        <Box sx={{ pb: 5 }}>
          <Typography variant="h4">Hi, Welcome back</Typography>
        </Box>
        <Grid container spacing={3}>
          <Grid item xs={12} sm={6} md={3}>
            <AppWeeklySales />
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <AppNewUsers />
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <AppItemOrders />
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <AppBugReports />
          </Grid>

          <Grid item xs={12} md={6} lg={8}>
            <AppWebsiteVisits />
          </Grid>

          <Grid item xs={12} md={6} lg={4}>
            <AppCurrentVisits />
          </Grid>

          <Grid item xs={6} md={3} lg={6}>
            <AppConversionRates category="Food" chartData={FoodData} />
          </Grid>

          <Grid item xs={6} md={3} lg={6}>
            <AppConversionRates category="Clothing" chartData={ClothingData} />
          </Grid>

          <Grid item xs={6} md={3} lg={6}>
            <AppConversionRates category="Electronics" chartData={ElectronicsData} />
          </Grid>

          <Grid item xs={6} md={3} lg={6}>
            <AppConversionRates category="Healthcare & Wellness" chartData={HealthcareData} />
          </Grid>

          <Grid item xs={12} md={12} lg={6}>
            <AppOrderTimeline />
          </Grid>
        </Grid>
      </Container>
    </Page>
  );
}
