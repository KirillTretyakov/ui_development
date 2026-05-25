import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
  Legend,
} from "recharts";

const modelMetricsData = [
  {
    metric: "Pseudo@5",
    "Подбор по названию": 0.449,
    "Embeddings + LR": 0.541,
    "TF-IDF + LR": 0.713,
  },
  {
    metric: "Skill@5",
    "Подбор по названию": 0.253,
    "Embeddings + LR": 0.382,
    "TF-IDF + LR": 0.642,
  },
  {
    metric: "Exp@5",
    "Подбор по названию": 0.848,
    "Embeddings + LR": 0.864,
    "TF-IDF + LR": 0.855,
  },
];

function ModelComparisonChart() {
  return (
    <section className="model-section">
      <div className="model-chart-card">
        <h2>Сравнение моделей</h2>

        <p className="model-section-lead">
          Ниже показаны значения метрик для трех подходов к сопоставлению
          резюме и вакансий.
        </p>

        <div className="model-chart-wrapper">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart
              data={modelMetricsData}
              margin={{ top: 20, right: 24, left: 0, bottom: 8 }}
              barGap={6}
            >
              <CartesianGrid strokeDasharray="3 3" vertical={false} />
              <XAxis dataKey="metric" tick={{ fontSize: 13 }} />
              <YAxis domain={[0, 1]} tick={{ fontSize: 13 }} />
              <Tooltip />
              <Legend />

              <Bar
                dataKey="Подбор по названию"
                fill="#A5B4FC"
                radius={[8, 8, 0, 0]}
              />
              <Bar
                dataKey="Embeddings + LR"
                fill="#7C3AED"
                radius={[8, 8, 0, 0]}
              />
              <Bar
                dataKey="TF-IDF + LR"
                fill="#4338CA"
                radius={[8, 8, 0, 0]}
              />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="model-description-grid">
          <div className="model-description-item">
            <h3>Подбор по названию</h3>
            <p>
              Базовый подход: оценивает близость резюме и вакансии по названию
              желаемой и требуемой должности.
            </p>
          </div>

          <div className="model-description-item">
            <h3>Embeddings + LR</h3>
            <p>
              Тексты переводятся в эмбеддинги, а логистическая регрессия
              обучается отличать подходящие пары от неподходящих.
            </p>
          </div>

          <div className="model-description-item">
            <h3>TF-IDF + LR</h3>
            <p>
              Тексты пары представляются через TF-IDF-признаки, после чего
              Logistic Regression формирует итоговый score.
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}

export default ModelComparisonChart;