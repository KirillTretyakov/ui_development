import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
} from "recharts";

const topResumeTitlesData = [
  { title: "аналитик данных", count: 2300 },
  { title: "data scientist", count: 1600 },
  { title: "data analyst", count: 540 },
  { title: "data engineer", count: 430 },
  { title: "продуктовый аналитик", count: 220 },
  { title: "junior data scientist", count: 130 },
  { title: "bi-аналитик", count: 115 },
  { title: "ml engineer", count: 90 },
];

function TopResumeTitlesChart() {
  return (
    <div className="chart-card">
      <h3>Топ желаемых должностей</h3>

        <ResponsiveContainer width="100%" height={320}>
        <BarChart
            data={topResumeTitlesData}
            layout="vertical"
            margin={{ top: 10, right: 20, left: 10, bottom: 10 }}
        >
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis type="number" />
            <YAxis
            type="category"
            dataKey="title"
            width={85}
            tick={{ fontSize: 11 }}
            />
            <Tooltip />
            <Bar dataKey="count" fill="#5B4BEA" radius={[0, 8, 8, 0]} />
        </BarChart>
        </ResponsiveContainer>
    </div>
  );
}

export default TopResumeTitlesChart;