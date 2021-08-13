import faker from 'faker';
import { sample } from 'lodash';
// utils
import { mockImgAvatar } from '../utils/mockImages';

// ----------------------------------------------------------------------

const users = [...Array(24)].map((_, index) => ({
  bill_id: faker.datatype.uuid(),
  avatarUrl: mockImgAvatar(index + 1),
  name: faker.name.findName(),
  amount: faker.finance.amount(1000, 10000),
  company: faker.company.companyName(),
  timeStamp: faker.date.past(2),
  isVerified: faker.datatype.boolean(),
  category: sample(['Food', 'Clothing', 'Electronics', 'Health & Wellness']),
  brand: sample([
    'Dairy Products',
    'Fruits',
    'Vegetables',
    'Cereals',
    'Grains',
    'Instant Food',
    'Drinks'
  ]),
  status: sample(['success', 'pending']),
  role: sample([
    'Leader',
    'Hr Manager',
    'UI Designer',
    'UX Designer',
    'UI/UX Designer',
    'Project Manager',
    'Backend Developer',
    'Full Stack Designer',
    'Front End Developer',
    'Full Stack Developer'
  ]),
  store: sample([
    'Big Bazaar',
    'Metro Wholesale',
    'Royal Mart',
    'Reliance Stores',
    'Landmark',
    'Walmart',
    'Target'
  ])
}));

export default users;
