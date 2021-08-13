import { Icon } from '@iconify/react';
import dashboard from '@iconify/icons-ic/dashboard';
import transaction from '@iconify/icons-ant-design/ordered-list';
import pendingTransaction from '@iconify/icons-ic/baseline-pending-actions';

// ----------------------------------------------------------------------

const getIcon = (name) => <Icon icon={name} width={22} height={22} />;

const sidebarConfig = [
  {
    title: 'dashboard',
    path: '/dashboard',
    icon: getIcon(dashboard)
  },
  {
    title: 'All Transactions',
    path: '/transactions',
    icon: getIcon(transaction)
  },
  {
    title: 'Pending Transactions',
    path: '/pendingtransactions',
    icon: getIcon(pendingTransaction)
  }
];

export default sidebarConfig;
