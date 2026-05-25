import {
  PieChart,
  Pie,
  Tooltip,
  ResponsiveContainer,
  Cell,
  Legend,
} from "recharts";

const topSkillsData = [
  { skill: "SQL", count: 120 },
  { skill: "Python", count: 98 },
  { skill: "Excel", count: 75 },
  { skill: "Power BI", count: 63 },
  { skill: "Pandas", count: 51 },
];
const totalSkills = topSkillsData.reduce((sum, item) => sum + item.count, 0);
const COLORS = ["#3F2BDB", "#5B4BEA", "#7568F0", "#9B92F5", "#C7C2FA"];

function TopSkillsChart() {
  return (
    <div className="chart-card">
      <h3>Топ навыков</h3>

      <ResponsiveContainer width="100%" height={350}>
        <PieChart>
          <Pie
            data={topSkillsData}
            dataKey="count"
            nameKey="skill"
            cx="50%"
            cy="50%"
            outerRadius={120}
            label={({ percent }) => `${(percent * 100).toFixed(1)}%`}
          >
            {topSkillsData.map((entry, index) => (
              <Cell
                key={`cell-${index}`}
                fill={COLORS[index % COLORS.length]}
              />
            ))}
          </Pie>

          <Tooltip />
          <Legend />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}

export default TopSkillsChart;