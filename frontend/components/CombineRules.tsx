import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "c/components/ui/card";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "c/components/ui/select";
import { Input } from "c/components/ui/input";
import { Textarea } from "c/components/ui/textarea";
import { Button } from "c/components/ui/button";

interface Rule {
  id: string;
  name: string;
}

const CombineRules: React.FC = () => {
    const [rules, setRules] = useState<Rule[]>([]);
    const [selectedRules, setSelectedRules] = useState<string[]>([]);
    const [operator, setOperator] = useState<'AND' | 'OR'>('AND');
    const [name, setName] = useState<string>('');
    const [description, setDescription] = useState<string>('');
    const [loading, setLoading] = useState<boolean>(false);
    const [error, setError] = useState<string>('');
    const [success, setSuccess] = useState<string>('');
  
    useEffect(() => {
      fetch('http://localhost:8000/api/v1/fetch/')
        .then(res => res.json())
        .then(data => setRules(data.rules))
        .catch(err => console.error('Error fetching rules:', err));
    }, []);
  
    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
      e.preventDefault();
      setLoading(true);
      setError('');
      setSuccess('');
  
      try {
        const response = await fetch('http://localhost:8000/api/v1/combine/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            rule_ids: selectedRules,
            name,
            description,
            operator,
          }),
        });
  
        if (!response.ok) {
          throw new Error('Failed to combine rules');
        }
  
        setSuccess('Rules combined successfully!');
        setSelectedRules([]);
        setName('');
        setDescription('');
      } catch (error) {
        setError(error instanceof Error ? error.message : 'An unknown error occurred');
      } finally {
        setLoading(false);
      }
    };
  
    return (
      <Card>
        <CardHeader>
          <CardTitle>Combine Rules</CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700">Select Rules</label>
              <div className="mt-2 space-y-2">
                {rules.map((rule) => (
                  <label key={rule.id} className="flex items-center">
                    <input
                      type="checkbox"
                      checked={selectedRules.includes(rule.id)}
                      onChange={(e: React.ChangeEvent<HTMLInputElement>) => {
                        if (e.target.checked) {
                          setSelectedRules([...selectedRules, rule.id]);
                        } else {
                          setSelectedRules(selectedRules.filter(id => id !== rule.id));
                        }
                      }}
                      className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                    />
                    <span className="ml-2">{rule.name}</span>
                  </label>
                ))}
              </div>
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium">Operator</label>
              <Select value={operator} onValueChange={(value: 'AND' | 'OR') => setOperator(value)}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="AND">AND</SelectItem>
                  <SelectItem value="OR">OR</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">New Rule Name</label>
              <Input
                value={name}
                onChange={(e: React.ChangeEvent<HTMLInputElement>) => setName(e.target.value)}
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">Description</label>
              <Textarea
                value={description}
                onChange={(e: React.ChangeEvent<HTMLTextAreaElement>) => setDescription(e.target.value)}
                rows={3}
              />
            </div>
            {error && <div className="text-red-500">{error}</div>}
            {success && <div className="text-green-500">{success}</div>}
            <Button type="submit" disabled={loading || selectedRules.length < 2}>
              {loading ? 'Combining...' : 'Combine Rules'}
            </Button>
          </form>
        </CardContent>
      </Card>
    );
};

export default CombineRules;
