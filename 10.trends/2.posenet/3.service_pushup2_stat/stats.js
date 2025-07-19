window.onload = function () {
    const labels = [];
    const values = [];

    const keys = Object.keys(localStorage)
        .filter((k) => /^\d{4}-\d{2}-\d{2}$/.test(k))
        .sort();

    keys.forEach((key) => {
        labels.push(key);
        values.push(parseInt(localStorage.getItem(key)));
    });

    const ctx = document.getElementById('myChart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [
                {
                    label: '횟수',
                    data: values,
                    backgroundColor: 'rgba(54, 162, 235, 0.6)',
                },
            ],
        },
        options: {
            responsive: true,
            scales: {
                y: { beginAtZero: true },
            },
        },
    });
};
