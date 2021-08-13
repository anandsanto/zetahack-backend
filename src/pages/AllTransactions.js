import { filter } from 'lodash';
import { Icon } from '@iconify/react';
import { useState } from 'react';
import roundFilterList from '@iconify/icons-ic/round-filter-list';
import { Link as RouterLink } from 'react-router-dom';
// material
import {
  Card,
  Table,
  Stack,
  Button,
  Checkbox,
  TableRow,
  TableBody,
  TableCell,
  Container,
  Typography,
  TableContainer,
  TablePagination
} from '@material-ui/core';
// components
import Page from '../components/Page';
import Label from '../components/Label';
import Scrollbar from '../components/Scrollbar';
import SearchNotFound from '../components/SearchNotFound';
import { UserListHead, UserListToolbar, UserMoreMenu } from '../components/_dashboard/user';
//
import USERLIST from '../_mocks_/user';

// ----------------------------------------------------------------------

const TABLE_HEAD = [
  { id: 'bill_id', label: 'Bill No.', alignRight: false },
  { id: 'store_id', label: 'Store Name', alignRight: false },
  { id: 'total_amount', label: 'Total Amount', alignRight: false },
  { id: 'ts', label: 'Timestamp', alignRight: false },
  { id: 'status', label: 'Status', alignRight: false },
  { id: 'isVerified', label: 'More info', alignRight: false },
  { id: '' }
];

const storeLabels = [
  { id: 'category', label: 'Product Category', alignRight: false },
  { id: 'total_amount', label: 'Total Amount', alignRight: true },
  { id: 'status', label: 'Timestamp', alignRight: false },
  { id: 'moreinfo', label: 'More info', alignRight: false }
];

const categoryLabels = [
  { id: 'brand', label: 'Product Name', alignRight: false },
  { id: 'total_amount', label: 'Total Amount', alignRight: true },
  { id: 'status', label: 'Timestamp', alignRight: false },
  { id: 'store', label: 'Store', alignRight: false },
  { id: 'moreinfo', label: 'More info', alignRight: false }
];

const brandLabels = [
  { id: 'store', label: 'Store', alignRight: false },
  { id: 'qty', label: 'Quantity', alignRight: false },
  { id: 'total_amount', label: 'Total Amount', alignRight: true },
  { id: 'ts', label: 'Timestamp', alignRight: false },
  { id: 'moreinfo', label: 'More info', alignRight: false }
];
// ----------------------------------------------------------------------

function descendingComparator(a, b, orderBy) {
  if (b[orderBy] < a[orderBy]) {
    return -1;
  }
  if (b[orderBy] > a[orderBy]) {
    return 1;
  }
  return 0;
}

function getComparator(order, orderBy) {
  return order === 'desc'
    ? (a, b) => descendingComparator(a, b, orderBy)
    : (a, b) => -descendingComparator(a, b, orderBy);
}

function applySortFilter(array, comparator, query) {
  const stabilizedThis = array.map((el, index) => [el, index]);
  stabilizedThis.sort((a, b) => {
    const order = comparator(a[0], b[0]);
    if (order !== 0) return order;
    return a[1] - b[1];
  });
  if (query) {
    return filter(array, (_user) => _user.name.toLowerCase().indexOf(query.toLowerCase()) !== -1);
  }
  return stabilizedThis.map((el) => el[0]);
}

export default function AllTransactions() {
  const [page, setPage] = useState(0);
  const [order, setOrder] = useState('asc');
  const [selected, setSelected] = useState([]);
  const [orderBy, setOrderBy] = useState('name');
  const [filterName, setFilterName] = useState('');
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [filterView, setFilterView] = useState('default');
  const handleRequestSort = (event, property) => {
    const isAsc = orderBy === property && order === 'asc';
    setOrder(isAsc ? 'desc' : 'asc');
    setOrderBy(property);
  };

  const handleSelectAllClick = (event) => {
    if (event.target.checked) {
      const newSelecteds = USERLIST.map((n) => n.name);
      setSelected(newSelecteds);
      return;
    }
    setSelected([]);
  };

  const handleClick = (event, name) => {
    const selectedIndex = selected.indexOf(name);
    let newSelected = [];
    if (selectedIndex === -1) {
      newSelected = newSelected.concat(selected, name);
    } else if (selectedIndex === 0) {
      newSelected = newSelected.concat(selected.slice(1));
    } else if (selectedIndex === selected.length - 1) {
      newSelected = newSelected.concat(selected.slice(0, -1));
    } else if (selectedIndex > 0) {
      newSelected = newSelected.concat(
        selected.slice(0, selectedIndex),
        selected.slice(selectedIndex + 1)
      );
    }
    setSelected(newSelected);
  };

  const handleChangePage = (event, newPage) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };

  const handleFilterByName = (event) => {
    setFilterName(event.target.value);
  };

  const emptyRows = page > 0 ? Math.max(0, (1 + page) * rowsPerPage - USERLIST.length) : 0;

  const filteredUsers = applySortFilter(USERLIST, getComparator(order, orderBy), filterName);

  const isUserNotFound = filteredUsers.length === 0;

  return (
    <Page title="Pending Transaction">
      <Container>
        <Stack direction="row-reverse" alignItems="center" justifyContent="space-between" mb={5}>
          <Stack direction="row" alignItems="center" justifyContent="space-between">
            <Stack padding="10px">
              <Button
                m="3rem"
                variant="contained"
                component={RouterLink}
                to="#store"
                onClick={() => setFilterView('store')}
                startIcon={<Icon icon={roundFilterList} />}
              >
                Filter by Store
              </Button>
            </Stack>
            <Stack padding="10px">
              <Button
                variant="contained"
                component={RouterLink}
                to="#category"
                onClick={() => setFilterView('category')}
                startIcon={<Icon icon={roundFilterList} />}
              >
                Filter by Category
              </Button>
            </Stack>
            <Stack padding="10px">
              <Button
                variant="contained"
                component={RouterLink}
                to="#brand"
                onClick={() => setFilterView('brand')}
                startIcon={<Icon icon={roundFilterList} />}
              >
                Filter by Brand
              </Button>
            </Stack>
          </Stack>
          <Stack xs={3}>
            <Typography variant="h4" gutterBottom>
              All Transactions
            </Typography>
          </Stack>
        </Stack>

        <Stack direction="row" alignItems="center" justifyContent="flex-start" mb={5}>
          {filterView !== 'default' && <>Filters: </>}
          {filterView === 'brand' && (
            <Stack padding="10px">
              <Label variant="ghost" color="info">
                Dairy Products
              </Label>
            </Stack>
          )}
          {filterView === 'category' && (
            <Stack padding="10px">
              <Label variant="ghost" color="error">
                Food
              </Label>
            </Stack>
          )}
          {filterView === 'store' && (
            <Stack padding="10px">
              <Label variant="ghost" color="warning">
                Big Bazaar
              </Label>
            </Stack>
          )}
          {filterView !== 'default' && (
            <a
              href=""
              onClick={() => setFilterView('default')}
              style={{ color: '#59bfff', paddingLeft: '10px' }}
            >
              clear
            </a>
          )}
        </Stack>

        <Card>
          <UserListToolbar
            numSelected={selected.length}
            filterName={filterName}
            onFilterName={handleFilterByName}
          />

          {filterView === 'default' && (
            <>
              <Scrollbar>
                <TableContainer sx={{ minWidth: 800 }}>
                  <Table>
                    <UserListHead
                      order={order}
                      orderBy={orderBy}
                      headLabel={TABLE_HEAD}
                      rowCount={USERLIST.length}
                      numSelected={selected.length}
                      onRequestSort={handleRequestSort}
                      onSelectAllClick={handleSelectAllClick}
                    />
                    <TableBody>
                      {filteredUsers
                        .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
                        .map((row) => {
                          const { id, name } = row;
                          const isItemSelected = selected.indexOf(name) !== -1;
                          return (
                            <TableRow
                              hover
                              key={id}
                              tabIndex={-1}
                              role="checkbox"
                              selected={isItemSelected}
                              aria-checked={isItemSelected}
                            >
                              <TableCell padding="checkbox">
                                <Checkbox
                                  checked={isItemSelected}
                                  onChange={(event) => handleClick(event, name)}
                                />
                              </TableCell>
                              <TableCell component="th" scope="row">
                                <Stack direction="row" alignItems="center" spacing={2}>
                                  <Typography variant="subtitle2" noWrap>
                                    {row.bill_id}
                                  </Typography>
                                </Stack>
                              </TableCell>
                              <TableCell align="left">{row.store}</TableCell>
                              <TableCell align="right">${row.amount}</TableCell>
                              <TableCell align="left">
                                {new Date(row.timeStamp).toLocaleString()}
                              </TableCell>
                              <TableCell align="left">
                                <Label variant="ghost" color="success">
                                  Success
                                </Label>
                              </TableCell>

                              <TableCell align="center">
                                <UserMoreMenu />
                              </TableCell>
                            </TableRow>
                          );
                        })}
                      {emptyRows > 0 && (
                        <TableRow style={{ height: 53 * emptyRows }}>
                          <TableCell colSpan={6} />
                        </TableRow>
                      )}
                    </TableBody>
                    {isUserNotFound && (
                      <TableBody>
                        <TableRow>
                          <TableCell align="center" colSpan={6} sx={{ py: 3 }}>
                            <SearchNotFound searchQuery={filterName} />
                          </TableCell>
                        </TableRow>
                      </TableBody>
                    )}
                  </Table>
                </TableContainer>
              </Scrollbar>
            </>
          )}

          {filterView === 'store' && (
            <Scrollbar>
              <TableContainer sx={{ minWidth: 800 }}>
                <Table>
                  <UserListHead
                    order={order}
                    orderBy={orderBy}
                    headLabel={storeLabels}
                    rowCount={USERLIST.length}
                    numSelected={selected.length}
                    onRequestSort={handleRequestSort}
                    onSelectAllClick={handleSelectAllClick}
                  />
                  <TableBody>
                    {filteredUsers
                      .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
                      .map((row) => {
                        const { id, name } = row;
                        const isItemSelected = selected.indexOf(name) !== -1;
                        return (
                          <TableRow
                            hover
                            key={id}
                            tabIndex={-1}
                            role="checkbox"
                            selected={isItemSelected}
                            aria-checked={isItemSelected}
                          >
                            <TableCell padding="checkbox">
                              <Checkbox
                                checked={isItemSelected}
                                onChange={(event) => handleClick(event, name)}
                              />
                            </TableCell>
                            <TableCell component="th" scope="row">
                              <Stack direction="row" alignItems="Left" spacing={2}>
                                <Typography variant="subtitle2" noWrap>
                                  {row.category}
                                </Typography>
                              </Stack>
                            </TableCell>
                            <TableCell align="right">${row.amount}</TableCell>
                            <TableCell align="left">
                              {new Date(row.timeStamp).toLocaleString()}
                            </TableCell>
                            <TableCell align="left">
                              <UserMoreMenu />
                            </TableCell>
                          </TableRow>
                        );
                      })}
                    {emptyRows > 0 && (
                      <TableRow style={{ height: 53 * emptyRows }}>
                        <TableCell colSpan={6} />
                      </TableRow>
                    )}
                  </TableBody>
                  {isUserNotFound && (
                    <TableBody>
                      <TableRow>
                        <TableCell align="center" colSpan={6} sx={{ py: 3 }}>
                          <SearchNotFound searchQuery={filterName} />
                        </TableCell>
                      </TableRow>
                    </TableBody>
                  )}
                </Table>
              </TableContainer>
            </Scrollbar>
          )}
          {filterView === 'category' && (
            <Scrollbar>
              <TableContainer sx={{ minWidth: 800 }}>
                <Table>
                  <UserListHead
                    order={order}
                    orderBy={orderBy}
                    headLabel={categoryLabels}
                    rowCount={USERLIST.length}
                    numSelected={selected.length}
                    onRequestSort={handleRequestSort}
                    onSelectAllClick={handleSelectAllClick}
                  />
                  <TableBody>
                    {filteredUsers
                      .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
                      .map((row) => {
                        const { id, name } = row;
                        const isItemSelected = selected.indexOf(name) !== -1;
                        return (
                          <TableRow
                            hover
                            key={id}
                            tabIndex={-1}
                            role="checkbox"
                            selected={isItemSelected}
                            aria-checked={isItemSelected}
                          >
                            <TableCell padding="checkbox">
                              <Checkbox
                                checked={isItemSelected}
                                onChange={(event) => handleClick(event, name)}
                              />
                            </TableCell>
                            <TableCell component="th" scope="row">
                              <Stack direction="row" alignItems="Left" spacing={2}>
                                <Typography variant="subtitle2" noWrap>
                                  {row.brand}
                                </Typography>
                              </Stack>
                            </TableCell>
                            <TableCell align="right">${row.amount}</TableCell>
                            <TableCell align="left">
                              {new Date(row.timeStamp).toLocaleString()}
                            </TableCell>
                            <TableCell align="left">{row.store}</TableCell>
                            <TableCell align="left">
                              <UserMoreMenu />
                            </TableCell>
                          </TableRow>
                        );
                      })}
                    {emptyRows > 0 && (
                      <TableRow style={{ height: 53 * emptyRows }}>
                        <TableCell colSpan={6} />
                      </TableRow>
                    )}
                  </TableBody>
                  {isUserNotFound && (
                    <TableBody>
                      <TableRow>
                        <TableCell align="center" colSpan={6} sx={{ py: 3 }}>
                          <SearchNotFound searchQuery={filterName} />
                        </TableCell>
                      </TableRow>
                    </TableBody>
                  )}
                </Table>
              </TableContainer>
            </Scrollbar>
          )}

          {filterView === 'brand' && (
            <Scrollbar>
              <TableContainer sx={{ minWidth: 800 }}>
                <Table>
                  <UserListHead
                    order={order}
                    orderBy={orderBy}
                    headLabel={brandLabels}
                    rowCount={USERLIST.length}
                    numSelected={selected.length}
                    onRequestSort={handleRequestSort}
                    onSelectAllClick={handleSelectAllClick}
                  />
                  <TableBody>
                    {filteredUsers
                      .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
                      .map((row) => {
                        const { id, name } = row;
                        const isItemSelected = selected.indexOf(name) !== -1;
                        return (
                          <TableRow
                            hover
                            key={id}
                            tabIndex={-1}
                            role="checkbox"
                            selected={isItemSelected}
                            aria-checked={isItemSelected}
                          >
                            <TableCell padding="checkbox">
                              <Checkbox
                                checked={isItemSelected}
                                onChange={(event) => handleClick(event, name)}
                              />
                            </TableCell>
                            <TableCell component="th" scope="row">
                              <Stack direction="row" alignItems="Left" spacing={2}>
                                <Typography variant="subtitle2" noWrap>
                                  {row.store}
                                </Typography>
                              </Stack>
                            </TableCell>
                            <TableCell align="left">2 Ltrs</TableCell>
                            <TableCell align="right">$ 50.45</TableCell>
                            <TableCell align="left">
                              {new Date(row.timeStamp).toLocaleString()}
                            </TableCell>
                            <TableCell align="left">
                              <UserMoreMenu />
                            </TableCell>
                          </TableRow>
                        );
                      })}
                    {emptyRows > 0 && (
                      <TableRow style={{ height: 53 * emptyRows }}>
                        <TableCell colSpan={6} />
                      </TableRow>
                    )}
                  </TableBody>
                  {isUserNotFound && (
                    <TableBody>
                      <TableRow>
                        <TableCell align="center" colSpan={6} sx={{ py: 3 }}>
                          <SearchNotFound searchQuery={filterName} />
                        </TableCell>
                      </TableRow>
                    </TableBody>
                  )}
                </Table>
              </TableContainer>
            </Scrollbar>
          )}

          <TablePagination
            rowsPerPageOptions={[5, 10, 25]}
            component="div"
            count={USERLIST.length}
            rowsPerPage={rowsPerPage}
            page={page}
            onPageChange={handleChangePage}
            onRowsPerPageChange={handleChangeRowsPerPage}
          />
        </Card>
      </Container>
    </Page>
  );
}
