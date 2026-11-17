import java.util.*;

public class A2_JobSequencing {
    public static class Job {
        public String id;
        public int deadline;
        public int profit;

        public Job(String id, int deadline, int profit) {
            this.id = id;
            this.deadline = deadline;
            this.profit = profit;
        }
    }

    public static class ScheduleResult {
        public Job[] slots;
        public int totalProfit;

        public ScheduleResult(Job[] slots, int totalProfit) {
            this.slots = slots;
            this.totalProfit = totalProfit;
        }
    }

    public static ScheduleResult scheduleJobs(List<Job> jobs) {
        List<Job> valid = new ArrayList<>();
        int maxDeadline = 0;
        for (Job j : jobs) {
            if (j.deadline > 0 && j.profit > 0) {
                valid.add(j);
                if (j.deadline > maxDeadline) {
                    maxDeadline = j.deadline;
                }
            }
        }
        if (valid.isEmpty()) {
            return new ScheduleResult(new Job[0], 0);
        }

        int horizon = Math.min(valid.size(), maxDeadline);
        Job[] slots = new Job[horizon];
        int totalProfit = 0;

        // Sort descending by profit
        valid.sort((a, b) -> Integer.compare(b.profit, a.profit));

        for (Job job : valid) {
            int maxSlot = Math.min(job.deadline, horizon) - 1;
            for (int s = maxSlot; s >= 0; s--) {
                if (slots[s] == null) {
                    slots[s] = job;
                    totalProfit += job.profit;
                    break;
                }
            }
        }

        return new ScheduleResult(slots, totalProfit);
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Number of jobs: ");
        if (!scanner.hasNextInt()) return;
        int n = scanner.nextInt();
        scanner.nextLine(); // consume newline

        List<Job> jobs = new ArrayList<>();
        for (int i = 0; i < n; i++) {
            System.out.print("Job " + (i + 1) + " (ID Deadline Profit): ");
            String line = "";
            while (line.isEmpty() && scanner.hasNextLine()) {
                line = scanner.nextLine().trim();
            }
            String[] parts = line.split("\\s+");
            String id;
            int deadline;
            int profit;

            if (parts.length >= 3) {
                id = parts[0];
                deadline = Integer.parseInt(parts[1]);
                profit = Integer.parseInt(parts[2]);
            } else if (parts.length == 2) {
                id = "J" + (i + 1);
                deadline = Integer.parseInt(parts[0]);
                profit = Integer.parseInt(parts[1]);
            } else if (parts.length == 1 && !parts[0].isEmpty()) {
                id = parts[0];
                System.out.print("  Deadline for " + id + ": ");
                deadline = scanner.nextInt();
                System.out.print("  Profit for " + id + ": ");
                profit = scanner.nextInt();
                if (scanner.hasNextLine()) scanner.nextLine();
            } else {
                id = "J" + (i + 1);
                System.out.print("  Deadline for Job " + (i + 1) + ": ");
                deadline = scanner.nextInt();
                System.out.print("  Profit for Job " + (i + 1) + ": ");
                profit = scanner.nextInt();
                if (scanner.hasNextLine()) scanner.nextLine();
            }
            jobs.add(new Job(id, deadline, profit));
        }

        ScheduleResult result = scheduleJobs(jobs);
        for (int time = 0; time < result.slots.length; time++) {
            Job job = result.slots[time];
            System.out.println("Slot " + (time + 1) + " : " + (job != null ? job.id : "Idle"));
        }
        System.out.println("Maximum profit: " + result.totalProfit);
    }
}
