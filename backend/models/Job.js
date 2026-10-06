const mongoose = require("mongoose");

const jobSchema = new mongoose.Schema({
    title: {
        type: String,
        required: true
    },

    company: {
        type: String,
        required: true
    },

    location: {
        type: String,
        required: true
    },

    jobType: {
        type: String,
        enum: ["Full Time", "Part Time", "Internship"],
        required: true
    },

    salary: {
        min: {
            type: Number,
            required: true
        },
        max: {
            type: Number,
            required: true
        }
    },

    skills: {
        type: [String],
        required: true
    },

    experience: {
        min: {
            type: Number,
            required: true
        },
        max: {
            type: Number,
            required: true
        }
    },

    description: {
        type: String,
        required: true
    },

    postedAt: {
        type: Date,
        default: Date.now
    }
});

module.exports = mongoose.model("Job", jobSchema);