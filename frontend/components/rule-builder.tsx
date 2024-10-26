import React, { useState } from 'react';
import { 
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue 
} from "c/components/ui/select";
import { Button } from "c/components/ui/button";
import { Input } from "c/components/ui/input";
import { Plus, X } from 'lucide-react';

interface Field {
  id: string;
  label: string;
  type: 'number' | 'string';
}

interface Operator {
  id: string;
  label: string;
}

interface Condition {
  field: string;
  operator: string;
  value: string;
  connector: 'AND' | 'OR';
}

interface RuleBuilderProps {
  onBuildComplete: (ruleString: string) => void;
}

const RuleBuilder: React.FC<RuleBuilderProps> = ({ onBuildComplete }) => {
  const [conditions, setConditions] = useState<Condition[]>([{
    field: '',
    operator: '',
    value: '',
    connector: 'AND'
  }]);

  const fields: Field[] = [
    { id: 'age', label: 'Age', type: 'number' },
    { id: 'department', label: 'Department', type: 'string' },
    { id: 'salary', label: 'Salary', type: 'number' },
    { id: 'experience', label: 'Experience', type: 'number' }
  ];

  const operators: Operator[] = [
    { id: '>', label: 'Greater than' },
    { id: '<', label: 'Less than' },
    { id: '=', label: 'Equals' },
    { id: '>=', label: 'Greater than or equal' },
    { id: '<=', label: 'Less than or equal' },
    { id: '!=', label: 'Not equal' }
  ];

  const addCondition = () => {
    setConditions([...conditions, {
      field: '',
      operator: '',
      value: '',
      connector: 'AND'
    }]);
  };

  const removeCondition = (index: number) => {
    const newConditions = conditions.filter((_, i) => i !== index);
    setConditions(newConditions);
  };

  const updateCondition = (index: number, field: keyof Condition, value: string) => {
    const newConditions = [...conditions];
    newConditions[index] = { ...newConditions[index], [field]: value };
    setConditions(newConditions);
  };

  const buildRuleString = () => {
    return conditions.map((condition, index) => {
      const { field, operator, value, connector } = condition;
      const isString = fields.find(f => f.id === field)?.type === 'string';
      const valueStr = isString ? `'${value}'` : value;
      const conditionStr = `${field} ${operator} ${valueStr}`;
      
      return index === conditions.length - 1 
        ? conditionStr 
        : `${conditionStr} ${connector}`;
    }).join(' ');
  };

  return (
    <div className="space-y-4">
      {conditions.map((condition, index) => (
        <div key={index} className="flex gap-2 items-center">
          <Select
            value={condition.field}
            onValueChange={(value: string) => updateCondition(index, 'field', value)}
          >
            <SelectTrigger className="w-[200px]">
              <SelectValue placeholder="Select field" />
            </SelectTrigger>
            <SelectContent>
              {fields.map(field => (
                <SelectItem key={field.id} value={field.id}>
                  {field.label}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>

          <Select
            value={condition.operator}
            onValueChange={(value: string) => updateCondition(index, 'operator', value)}
          >
            <SelectTrigger className="w-[200px]">
              <SelectValue placeholder="Select operator" />
            </SelectTrigger>
            <SelectContent>
              {operators.map(op => (
                <SelectItem key={op.id} value={op.id}>
                  {op.label}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>

          <Input
            placeholder="Value"
            value={condition.value}
            onChange={(e: React.ChangeEvent<HTMLInputElement>) => updateCondition(index, 'value', e.target.value)}
            className="w-[200px]"
          />

          {index < conditions.length - 1 && (
            <Select
              value={condition.connector}
              onValueChange={(value: 'AND' | 'OR') => updateCondition(index, 'connector', value)}
            >
              <SelectTrigger className="w-[100px]">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="AND">AND</SelectItem>
                <SelectItem value="OR">OR</SelectItem>
              </SelectContent>
            </Select>
          )}

          <Button
            variant="destructive"
            size="icon"
            onClick={() => removeCondition(index)}
          >
            <X className="h-4 w-4" />
          </Button>
        </div>
      ))}

      <div className="flex gap-2">
        <Button onClick={addCondition} variant="outline">
          <Plus className="h-4 w-4 mr-2" />
          Add Condition
        </Button>
        <Button onClick={() => onBuildComplete(buildRuleString())}>
          Build Rule
        </Button>
      </div>
    </div>
  );
};

export default RuleBuilder;
