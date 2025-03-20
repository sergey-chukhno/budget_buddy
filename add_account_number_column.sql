USE billionnaires_budget_buddy;

-- Add account_number column if it doesn't exist
ALTER TABLE accounts ADD COLUMN IF NOT EXISTS account_number VARCHAR(20) AFTER account_name; 