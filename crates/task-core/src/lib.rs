use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};
use uuid::Uuid;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct TaskSpec {
    pub id: Uuid,
    pub name: String,
    pub args: serde_json::Value,
    pub kwargs: serde_json::Value,
    pub queue: String,
    pub retry: RetryPolicy,
    pub eta: Option<DateTime<Utc>>,
    pub timeout_seconds: Option<u64>,
    pub idempotency_key: Option<String>,
    pub created_at: DateTime<Utc>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct RetryPolicy {
    pub max_attempts: u32,
    pub attempt: u32,
    pub backoff_seconds: u64,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct TaskResult {
    pub id: Uuid,
    pub status: TaskStatus,
    pub started_at: Option<DateTime<Utc>>,
    pub finished_at: Option<DateTime<Utc>>,
    pub output: Option<serde_json::Value>,
    pub error: Option<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum TaskStatus {
    Queued,
    Running,
    Succeeded,
    Failed,
    Retrying,
    Revoked,
}
