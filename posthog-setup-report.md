<wizard-report>
# PostHog post-wizard report

The wizard has completed a deep integration of PostHog analytics into CareerBridge UK's FastAPI backend. A new `posthog_client.py` module was created to hold the singleton `Posthog` instance, which is initialised from environment variables and registered for graceful shutdown via `atexit`. The app's lifespan context manager in `main.py` calls `posthog_client.flush()` on shutdown to ensure in-flight events are delivered. User identification is performed on registration (with `posthog_client.set(...)` to persist person properties) and on login. Fourteen events are now tracked across six route files, covering the full user journey from signup to feedback.

| Event | Description | File |
|---|---|---|
| `user_registered` | New user successfully registers an account | `backend/app/api/routes/auth_routes.py` |
| `user_logged_in` | User successfully logs in | `backend/app/api/routes/auth_routes.py` |
| `password_reset_requested` | User requests a password reset code | `backend/app/api/routes/auth_routes.py` |
| `password_reset_completed` | User successfully resets their password | `backend/app/api/routes/auth_routes.py` |
| `cv_uploaded` | User uploads a CV file for parsing | `backend/app/api/routes/cv_routes.py` |
| `cv_analyzed` | AI successfully analyzes a user's CV | `backend/app/api/routes/cv_routes.py` |
| `cv_generated` | AI generates a UK-formatted CV | `backend/app/api/routes/cv_routes.py` |
| `cv_improved` | AI generates an improved CV from analysis | `backend/app/api/routes/cv_routes.py` |
| `job_matched` | AI matches a user's CV to a job description | `backend/app/api/routes/job_routes.py` |
| `jobs_searched` | User searches for live job listings | `backend/app/api/routes/job_routes.py` |
| `interview_prepared` | AI generates interview prep material | `backend/app/api/routes/interview_routes.py` |
| `mock_interview_completed` | User completes a mock interview exchange | `backend/app/api/routes/interview_routes.py` |
| `result_saved` | User saves an AI result to their history | `backend/app/api/routes/result_routes.py` |
| `feedback_submitted` | User submits in-app feedback | `backend/app/api/routes/feedback_routes.py` |

## Next steps

We've built some insights and a dashboard for you to keep an eye on user behavior, based on the events we just instrumented:

- [Analytics basics dashboard](https://us.posthog.com/project/431643/dashboard/1604778)
- [User Registrations & Logins](https://us.posthog.com/project/431643/insights/LAOYoOmC) — daily signups vs logins line chart
- [Feature Usage](https://us.posthog.com/project/431643/insights/KUd05LOj) — CV analysis, job matching, interview prep trends
- [Activation Funnel](https://us.posthog.com/project/431643/insights/g6je9tSU) — Register → CV Upload → CV Analyzed conversion steps
- [Results Saved by Feature](https://us.posthog.com/project/431643/insights/1TcTfD2j) — which AI features drive saves (broken down by feature type)
- [Feedback Submitted](https://us.posthog.com/project/431643/insights/uRLSxhz1) — weekly feedback submission volume

### Agent skill

We've left an agent skill folder in your project. You can use this context for further agent development when using Claude Code. This will help ensure the model provides the most up-to-date approaches for integrating PostHog.

</wizard-report>
