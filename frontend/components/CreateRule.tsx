import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "c/components/ui/card";
import { Input } from "c/components/ui/input";
import { Textarea } from "c/components/ui/textarea";
import { Button } from "c/components/ui/button";
import RuleBuilder from 'c/components/rule-builder';

interface FormData {
  name: string;
  description: string;
  rule_string: string;
}

const CreateRule: React.FC = () => {
  const [formData, setFormData] = useState<FormData>({
    name: '',
    description: '',
    rule_string: ''
  });
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string>('');
  const [success, setSuccess] = useState<string>('');

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess('');

    try {
      const response = await fetch('http://localhost:8000/api/v1/create/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        throw new Error('Failed to create rule');
      }

      setSuccess('Rule created successfully!');
      setFormData({ name: '', description: '', rule_string: '' });
    } catch (error) {
      setError(error instanceof Error ? error.message : 'An unknown error occurred');
    } finally {
      setLoading(false);
    }
  };

  const handleBuildComplete = (ruleString: string) => {
    setFormData(prev => ({ ...prev, rule_string: ruleString }));
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>Create Rule</CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700">Name</label>
            <Input
              value={formData.name}
              onChange={(e: React.ChangeEvent<HTMLInputElement>) => setFormData({ ...formData, name: e.target.value })}
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Description</label>
            <Textarea
              value={formData.description}
              onChange={(e: React.ChangeEvent<HTMLTextAreaElement>) => setFormData({ ...formData, description: e.target.value })}
              rows={3}
            />
          </div>
          <div className="space-y-4">
            <label className="block text-sm font-medium text-gray-700">Rule String</label>
            <RuleBuilder onBuildComplete={handleBuildComplete} />
            <div className="mt-4">
              <Textarea
                value={formData.rule_string}
                onChange={(e: React.ChangeEvent<HTMLTextAreaElement>) => setFormData({ ...formData, rule_string: e.target.value })}
                rows={5}
                placeholder="age > 30 AND department = 'Sales'"
                required
              />
            </div>
          </div>
          {error && <div className="text-red-500">{error}</div>}
          {success && <div className="text-green-500">{success}</div>}
          <Button type="submit" disabled={loading}>
            {loading ? 'Creating...' : 'Create Rule'}
          </Button>
        </form>
      </CardContent>
    </Card>
  );
};

export default CreateRule;
