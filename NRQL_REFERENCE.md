# 📊 NRQL Quick Reference Guide

Essential NRQL queries for effective New Relic monitoring through Cursor MCP.

## 🎯 Basic Query Structure

```sql
SELECT attribute(s)
FROM dataType  
WHERE conditions
SINCE timeframe
FACET groupBy
LIMIT number
```

## 📈 Performance Monitoring

### Application Performance
```sql
-- Average response time by application
SELECT average(duration) FROM Transaction SINCE 1 hour ago FACET appName

-- Throughput (requests per minute)  
SELECT rate(count(*), 1 minute) FROM Transaction SINCE 1 hour ago FACET appName

-- 95th percentile response times
SELECT percentile(duration, 95) FROM Transaction SINCE 1 day ago FACET appName

-- Slowest transactions
SELECT * FROM Transaction WHERE duration > 1 SINCE 1 hour ago LIMIT 20
```

### Database Performance
```sql
-- Slow database queries
SELECT average(databaseDuration) FROM Transaction WHERE databaseCallCount > 0 SINCE 1 hour ago FACET name

-- Database query count by application
SELECT sum(databaseCallCount) FROM Transaction SINCE 1 hour ago FACET appName

-- Most time-consuming database operations
SELECT * FROM DatabaseSample WHERE duration > 0.1 SINCE 1 hour ago LIMIT 10
```

### Infrastructure Metrics
```sql
-- CPU usage by host
SELECT average(cpuPercent) FROM SystemSample SINCE 1 hour ago FACET hostname

-- Memory usage
SELECT average(memoryUsedPercent) FROM SystemSample SINCE 1 hour ago FACET hostname

-- Disk I/O
SELECT average(diskIOWriteKbps), average(diskIOReadKbps) FROM SystemSample SINCE 1 hour ago FACET hostname
```

## 🚨 Error Monitoring

### Error Analysis
```sql
-- Error rate by application
SELECT percentage(count(*), WHERE error IS true) FROM Transaction SINCE 1 hour ago FACET appName

-- Most common errors
SELECT count(*) FROM TransactionError SINCE 1 day ago FACET error.message LIMIT 10

-- Error distribution by endpoint
SELECT count(*) FROM Transaction WHERE error IS true SINCE 1 hour ago FACET name LIMIT 20

-- 4xx and 5xx errors
SELECT count(*) FROM Transaction WHERE response.status >= 400 SINCE 1 hour ago FACET response.status, appName
```

### Log Analysis
```sql
-- Error logs by severity
SELECT count(*) FROM Log WHERE level IN ('ERROR', 'FATAL') SINCE 1 hour ago FACET level, message

-- Recent critical issues
SELECT * FROM Log WHERE level = 'ERROR' SINCE 30 minutes ago LIMIT 50

-- Application errors with context
SELECT timestamp, message, hostname FROM Log WHERE appName LIKE '%your-app%' AND level = 'ERROR' SINCE 1 hour ago
```

## 👤 User Experience

### Browser Performance
```sql
-- Page load times
SELECT average(duration) FROM PageView SINCE 1 hour ago FACET pageUrl

-- Browser compatibility
SELECT count(*) FROM PageView SINCE 1 day ago FACET userAgentName

-- Geographic performance
SELECT average(duration) FROM PageView SINCE 1 hour ago FACET regionCode, countryCode

-- Core Web Vitals
SELECT average(largestContentfulPaint), average(firstInputDelay), average(cumulativeLayoutShift) FROM PageViewTiming SINCE 1 day ago
```

### Mobile Performance
```sql
-- Mobile app performance
SELECT average(sessionDuration) FROM MobileSession SINCE 1 day ago FACET appName

-- Crash rate
SELECT percentage(count(*), WHERE category = 'Crash') FROM MobileSession SINCE 1 day ago FACET appName

-- Network performance by carrier
SELECT average(responseTime) FROM MobileRequest SINCE 1 day ago FACET carrier
```

## 💼 Business Intelligence

### Usage Analytics
```sql
-- Daily active users
SELECT uniqueCount(userId) FROM PageView SINCE 1 day ago

-- Most popular features/endpoints
SELECT count(*) FROM Transaction SINCE 1 day ago FACET name LIMIT 20

-- User session analysis
SELECT average(session.duration), count(*) FROM PageView SINCE 1 day ago FACET userAgentName

-- Revenue impact (custom attributes)
SELECT sum(revenue) FROM Transaction WHERE revenue IS NOT NULL SINCE 1 day ago FACET appName
```

### A/B Testing
```sql
-- Performance by experiment variant
SELECT average(duration) FROM PageView WHERE experiment.variant IS NOT NULL SINCE 1 day ago FACET experiment.variant

-- Conversion rates by test group
SELECT percentage(count(*), WHERE conversion = true) FROM PageView SINCE 1 week ago FACET testGroup
```

## 🕐 Time-based Analysis

### Trending Analysis
```sql
-- Hourly transaction volume
SELECT count(*) FROM Transaction SINCE 1 day ago TIMESERIES 1 hour

-- Daily error trends
SELECT count(*) FROM TransactionError SINCE 1 week ago TIMESERIES 1 day

-- Performance degradation detection
SELECT average(duration) FROM Transaction SINCE 1 week ago TIMESERIES 1 day FACET appName
```

### Peak Performance
```sql
-- Busiest hours
SELECT count(*) FROM Transaction SINCE 1 week ago FACET hourOf(timestamp)

-- Weekend vs weekday performance
SELECT average(duration) FROM Transaction SINCE 1 month ago FACET weekdayOf(timestamp)
```

## 🔍 Advanced Queries

### Alerting Conditions
```sql
-- Applications exceeding SLA
SELECT average(duration) FROM Transaction SINCE 5 minutes ago FACET appName HAVING average(duration) > 2

-- High error rate detection
SELECT percentage(count(*), WHERE error IS true) FROM Transaction SINCE 5 minutes ago FACET appName HAVING percentage(count(*), WHERE error IS true) > 5

-- Anomaly detection
SELECT average(duration) FROM Transaction SINCE 1 hour ago COMPARE WITH 1 week ago FACET appName
```

### Capacity Planning
```sql
-- Resource utilization trends
SELECT average(cpuPercent), average(memoryUsedPercent) FROM SystemSample SINCE 1 month ago TIMESERIES 1 day FACET hostname

-- Growth projections
SELECT rate(count(*), 1 day) FROM Transaction SINCE 1 month ago TIMESERIES 1 week FACET appName

-- Peak load analysis
SELECT max(rate(count(*), 1 minute)) FROM Transaction SINCE 1 week ago FACET appName
```

## 🎨 Data Visualization Tips

### For Dashboards
```sql
-- Use TIMESERIES for time-based charts
SELECT average(duration) FROM Transaction SINCE 1 day ago TIMESERIES FACET appName

-- Use FACET for grouping and comparison
SELECT count(*) FROM Transaction SINCE 1 hour ago FACET appName, name

-- Use percentile for SLA monitoring
SELECT percentile(duration, 50, 95, 99) FROM Transaction SINCE 1 day ago
```

### For Reports
```sql
-- Summary statistics
SELECT min(duration), max(duration), average(duration), percentile(duration, 95) FROM Transaction SINCE 1 week ago FACET appName

-- Comparative analysis
SELECT average(duration) FROM Transaction SINCE 1 day ago COMPARE WITH 1 week ago FACET appName
```

## 🔧 Optimization Queries

### Database Optimization
```sql
-- Identify slow queries
SELECT average(databaseDuration), count(*) FROM Transaction WHERE databaseDuration > 0.1 SINCE 1 day ago FACET databaseType, name

-- Connection pool analysis  
SELECT average(databaseCallCount) FROM Transaction SINCE 1 hour ago FACET appName, name

-- Query patterns
SELECT count(*) FROM Transaction WHERE databaseCallCount > 5 SINCE 1 day ago FACET name
```

### Performance Optimization
```sql
-- Memory leaks detection
SELECT average(memoryUsedBytes) FROM SystemSample SINCE 1 week ago TIMESERIES 1 day FACET hostname

-- Garbage collection impact
SELECT average(gcCumulativeTimeMs) FROM SystemSample SINCE 1 day ago FACET hostname

-- Thread pool analysis
SELECT average(threadCount) FROM SystemSample SINCE 1 day ago FACET hostname
```

## 💡 Pro Tips

1. **Always use time limits** - SINCE clause prevents resource exhaustion
2. **Limit results** - Use LIMIT to avoid overwhelming responses
3. **Group meaningfully** - FACET by relevant dimensions
4. **Compare periods** - Use COMPARE WITH for trend analysis
5. **Filter early** - WHERE clauses improve performance
6. **Use appropriate functions** - count(), average(), percentile() as needed

## ❓ Common Cursor Questions

### "Show me application health"
```sql
SELECT average(duration), percentage(count(*), WHERE error IS true), rate(count(*), 1 minute) FROM Transaction SINCE 1 hour ago FACET appName
```

### "Find performance issues"
```sql
SELECT name, average(duration), count(*) FROM Transaction WHERE duration > 2 SINCE 1 day ago FACET name LIMIT 20
```

### "What's causing errors?"
```sql
SELECT error.message, count(*) FROM TransactionError SINCE 1 day ago FACET error.message, appName LIMIT 10
```

---

**📚 Full NRQL documentation:** [docs.newrelic.com/docs/query-your-data/nrql-new-relic-query-language](https://docs.newrelic.com/docs/query-your-data/nrql-new-relic-query-language/)
