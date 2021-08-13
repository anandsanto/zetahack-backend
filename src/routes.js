import { Navigate, useRoutes } from 'react-router-dom';
import DashboardLayout from './layouts/dashboard';
import LogoOnlyLayout from './layouts/LogoOnlyLayout';
import Login from './pages/Login';
import Register from './pages/Register';
import DashboardApp from './pages/DashboardApp';
import User from './pages/User';
import NotFound from './pages/Page404';
import AllTransactions from './pages/AllTransactions';

export default function Router() {
  return useRoutes([
    {
      path: '/dashboard',
      element: <DashboardLayout />,
      children: [{ path: '/', element: <DashboardApp /> }]
    },
    {
      path: '/',
      element: <DashboardLayout />,
      children: [
        { path: '/', element: <DashboardApp /> },
        { path: 'transactions', element: <AllTransactions /> },
        { path: 'pendingtransactions', element: <User /> }
      ]
    },
    {
      path: '/',
      element: <LogoOnlyLayout />,
      children: [
        { path: 'login', element: <Login /> },
        { path: 'register', element: <Register /> },
        { path: '404', element: <NotFound /> },
        { path: '/', element: <Navigate to="/dashboard" /> },
        { path: '*', element: <Navigate to="/404" /> }
      ]
    },

    { path: '*', element: <Navigate to="/404" replace /> }
  ]);
}
