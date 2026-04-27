const MOCK_DELAY = 1000;

export const getDashboardStats = async () => {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve([
        { title: "Total Scans", value: "128", change: "+12%", isPositive: true, iconType: 'search' },
        { title: "Avg. Similarity", value: "18%", change: "-5%", isPositive: true, iconType: 'percent' },
        { title: "Documents Uploaded", value: "84", change: "+8%", isPositive: true, iconType: 'file' },
        { title: "Accuracy", value: "98.7%", change: "+2%", isPositive: true, iconType: 'check' },
      ]);
    }, MOCK_DELAY);
  });
};

export const getScanActivity = async (period = 'This Week') => {
  return new Promise((resolve) => {
    setTimeout(() => {
      let data;
      if (period === 'Last Week') {
        data = [
          { name: 'Mon', scans: 35 }, { name: 'Tue', scans: 42 }, { name: 'Wed', scans: 28 },
          { name: 'Thu', scans: 55 }, { name: 'Fri', scans: 38 }, { name: 'Sat', scans: 15 }, { name: 'Sun', scans: 20 },
        ];
      } else if (period === 'This Month') {
        data = [
          { name: 'Week 1', scans: 150 }, { name: 'Week 2', scans: 210 },
          { name: 'Week 3', scans: 180 }, { name: 'Week 4', scans: 250 },
        ];
      } else {
        // This Week
        data = [
          { name: 'Mon', scans: 45 }, { name: 'Tue', scans: 52 }, { name: 'Wed', scans: 38 },
          { name: 'Thu', scans: 65 }, { name: 'Fri', scans: 48 }, { name: 'Sat', scans: 25 }, { name: 'Sun', scans: 30 },
        ];
      }
      resolve(data);
    }, MOCK_DELAY);
  });
};

export const getRecentScans = async () => {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve([
        { id: 1, name: 'Research_Paper.pdf', similarity: 18, time: '2 min ago' },
        { id: 2, name: 'Assignment.docx', similarity: 22, time: '1 hour ago' },
        { id: 3, name: 'Thesis_Final.pdf', similarity: 9, time: '3 hours ago' },
        { id: 4, name: 'Article_Content.txt', similarity: 31, time: 'Yesterday' },
        { id: 5, name: 'Project_Report.pdf', similarity: 14, time: '2 days ago' },
      ]);
    }, MOCK_DELAY);
  });
};
