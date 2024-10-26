import { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "c/components/ui/card";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "c/components/ui/select";
import { Textarea } from "c/components/ui/textarea";
import { Button } from "c/components/ui/button";

const EvaluateRule = () => {
    const [rules, setRules] = useState([]);
    const [selectedRule, setSelectedRule] = useState('');
    const [jsonData, setJsonData] = useState('');
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
  
    useEffect(() => {
      fetch('http://localhost:8000/api/v1/fetch/')
        .then(res => res.json())
        .then(data => setRules(data.rules))
        .catch(err => console.error('Error fetching rules:', err));
    }, []);
  
    const handleSubmit = async (e) => {
      e.preventDefault();
      setLoading(true);
      setError('');
      setResult(null);
  
      try {
        let parsedData = JSON.parse(jsonData);
        
        const response = await fetch('http://localhost:8000/api/v1/evaluate/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            rule_id: selectedRule,
            data: parsedData
          }),
        });
  
        if (!response.ok) {
          throw new Error('Failed to evaluate rule');
        }
  
        const data = await response.json();
        setResult(data);
      } catch (error) {
        if (error instanceof SyntaxError) {
          setError('Invalid JSON format');
        } else {
          setError(error.message);
        }
      } finally {
        setLoading(false);
      }
    };
  
    return (
      <Card>
        <CardHeader>
          <CardTitle>Evaluate Rule</CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700">Select Rule</label>
              <Select value={selectedRule} onValueChange={setSelectedRule}>
                <SelectTrigger>
                  <SelectValue placeholder="Select a rule..." />
                </SelectTrigger>
                <SelectContent>
                  {rules.map((rule) => (
                    <SelectItem key={rule.id} value={rule.id}>{rule.name}</SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">JSON Data</label>
              <Textarea
                value={jsonData}
                onChange={(e) => setJsonData(e.target.value)}
                rows={5}
                placeholder={'{\n  "age": 35,\n  "department": "Sales",\n  "salary": 60000\n}'}
                required
              />
            </div>
            {error && <div className="text-red-500">{error}</div>}
            <Button type="submit" disabled={loading}>
              {loading ? 'Evaluating...' : 'Evaluate Rule'}
            </Button>
          </form>
  
          {result && (
            <Card className="mt-6">
              <CardHeader>
                <CardTitle>Evaluation Result</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  <p>Rule Name: {result.rule_name}</p>
                  <p>Rule String: <code className="bg-gray-100 px-2 py-1 rounded">{result.rule_string}</code></p>
                  <p className={`font-semibold ${result.result ? 'text-green-600' : 'text-red-600'}`}>
                    Result: {result.result ? 'True' : 'False'}
                  </p>
                </div>
              </CardContent>
            </Card>
          )}
        </CardContent>
      </Card>
    );
};

export default EvaluateRule;

