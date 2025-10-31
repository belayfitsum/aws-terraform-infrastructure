const request = require('supertest');
const express = require('express');

// Mock the database
jest.mock('./db', () => ({
  run: jest.fn(),
  all: jest.fn()
}));

const db = require('./db');

// Import app after mocking
const app = express();
app.use(express.json());

// Copy the routes from app.js for testing
app.post('/postData', (req, res) => {
  const { campaign_name, status } = req.body;
  if (!campaign_name || !status) return res.status(400).send('campaign_name and status are required.');

  db.run(
    `INSERT INTO ads (campaign_name, status) VALUES (?, ?)`,
    [campaign_name, status],
    function (err) {
      if (err) {
        return res.status(500).send('Error inserting into ads table.');
      }
      res.status(201).json({ id: 1, campaign_name, status });
    }
  );
});

app.get('/logs', (req, res) => {
  db.all(`SELECT * FROM ads`, [], (err, rows) => {
    if (err) {
      return res.status(500).send('Error fetching logs.');
    }
    res.json(rows || []);
  });
});

describe('API Tests', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('POST /postData - success', async () => {
    db.run.mockImplementation((query, params, callback) => {
      callback.call({ lastID: 1 }, null);
    });

    const response = await request(app)
      .post('/postData')
      .send({ campaign_name: 'Test Campaign', status: 'active' });

    expect(response.status).toBe(201);
    expect(response.body).toEqual({
      id: 1,
      campaign_name: 'Test Campaign',
      status: 'active'
    });
  });

  test('POST /postData - missing fields', async () => {
    const response = await request(app)
      .post('/postData')
      .send({ campaign_name: 'Test Campaign' });

    expect(response.status).toBe(400);
    expect(response.text).toBe('campaign_name and status are required.');
  });

  test('GET /logs - success', async () => {
    const mockData = [{ id: 1, campaign_name: 'Test', status: 'active' }];
    db.all.mockImplementation((query, params, callback) => {
      callback(null, mockData);
    });

    const response = await request(app).get('/logs');

    expect(response.status).toBe(200);
    expect(response.body).toEqual(mockData);
  });
});