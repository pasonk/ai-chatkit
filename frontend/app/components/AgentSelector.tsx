import React from 'react';
import { Select } from 'antd';

interface AgentSelectorProps {
  value: string;
  onChange: (value: string) => void;
}

const AgentSelector: React.FC<AgentSelectorProps> = ({ value, onChange }) => {
  return (
    <Select
      value={value}
      className="ml-2 mr-5 w-36"
      onChange={onChange}
      options={[{ value: "oa-assistant", label: "OA-ASSISTANT" }, { value: "multi-agent-supervisor", label: "MULTI-AGENT-SUPERVISOR" }]}
    />
  );
};

export default AgentSelector;