# Historical Court – Multi-Agent System

## Overview
This project is a multi-agent system built with Google ADK.
It simulates a historical court by analyzing a historical person
or event using Wikipedia.

## Architecture

Step 1 – Inquiry (Sequential)
- Ask user for a historical topic.

Step 2 – Investigation (Parallel)
- Admirer agent collects positive and achievement information.
- Critic agent collects negative and controversial information.

Step 3 – Trial & Review (Loop)
- Judge agent reviews both sides.
- If information is insufficient or unbalanced, agents are asked to research again.
- The loop ends using the exit_loop tool.

Step 4 – Verdict
- A neutral report is generated and saved as verdict.txt.

## State Management

The system uses the following state keys:
- topic
- pos_data
- neg_data

These keys are passed between agents using templating.

## Output
The system produces a file named verdict.txt containing
the final balanced report.

Note: The verdict.txt file represents the output produced by the system for the sample topic "Napoleon Bonaparte".
