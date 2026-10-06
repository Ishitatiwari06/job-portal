const express = require("express");
const Job = require("../models/Job");

const router = express.Router();

// Add a new job
router.post("/", async (req, res) => {
    try {
        const job = new Job(req.body);

        const savedJob = await job.save();

        res.status(201).json(savedJob);
    } catch (error) {
        res.status(400).json({
            message: "Failed to create job",
            error: error.message
        });
    }
});

// Get all jobs
router.get("/", async (req, res) => {
    try {
        const { title, location, jobType, skill, minSalary } = req.query;

        let filter = {};

        // Search by title
        if (title) {
            filter.title = { $regex: title, $options: "i" };
        }

        // Filter by location
        if (location) {
            filter.location = { $regex: location, $options: "i" };
        }

        // Filter by job type
        if (jobType) {
            filter.jobType = jobType;
        }

        // Filter by skill
        if (skill) {
            filter.skills = { $in: [skill] };
        }

        // Minimum salary
        if (minSalary) {
            filter["salary.min"] = { $gte: Number(minSalary) };
        }

        const jobs = await Job.find(filter);

        res.status(200).json(jobs);

    } catch (error) {
        res.status(500).json({
            message: "Failed to fetch jobs",
            error: error.message
        });
    }
});
// Get a single job by ID
router.get("/:id", async (req, res) => {
    try {
        const job = await Job.findById(req.params.id);

        if (!job) {
            return res.status(404).json({
                message: "Job not found"
            });
        }

        res.status(200).json(job);
    } catch (error) {
        res.status(500).json({
            message: "Failed to fetch job",
            error: error.message
        });
    }
});


// Update a job
router.put("/:id", async (req, res) => {
    try {
        const updatedJob = await Job.findByIdAndUpdate(
            req.params.id,
            req.body,
            { new: true, runValidators: true }
        );

        if (!updatedJob) {
            return res.status(404).json({
                message: "Job not found"
            });
        }

        res.status(200).json(updatedJob);
    } catch (error) {
        res.status(400).json({
            message: "Failed to update job",
            error: error.message
        });
    }
});


// Delete a job
router.delete("/:id", async (req, res) => {
    try {
        const deletedJob = await Job.findByIdAndDelete(req.params.id);

        if (!deletedJob) {
            return res.status(404).json({
                message: "Job not found"
            });
        }

        res.status(200).json({
            message: "Job deleted successfully"
        });
    } catch (error) {
        res.status(500).json({
            message: "Failed to delete job",
            error: error.message
        });
    }
});
module.exports = router;
