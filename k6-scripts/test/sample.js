import http from 'k6/http';
import { sleep } from 'k6';

export const options = {
  duration: '5m',
  vus: 15000,
  thresholds: {
    http_req_duration: ['p(95)<500'],
  },
};

export default function () {
  const res = http.get('https://test.k6.io');
  sleep(0.5);
}
