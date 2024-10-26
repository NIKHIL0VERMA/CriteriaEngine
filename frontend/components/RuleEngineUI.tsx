'use client'
import { Menu, PlusSquare, Combine, Play, List } from 'lucide-react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from "c/components/ui/tabs";
import RuleList from './RuleList';
import CreateRule from './CreateRule';
import CombineRules from './CombineRules';
import EvaluateRule from './EvaluateRule';

// Main layout component
const RuleEngineDashboard = () => {
  return (
    <div className="min-h-screen bg-gray-50">
      <main className="container mx-auto px-4 py-8">
        <Tabs defaultValue="list" className="space-y-6">
          <TabsList className="grid w-full grid-cols-2 sm:grid-cols-4 gap-2 sm:gap-4">
            <TabsTrigger value="list" className="flex items-center justify-center p-2 sm:p-4">
              <List className="h-4 w-4 mr-2" />
              <span className="text-xs sm:text-sm">Rule List</span>
            </TabsTrigger>
            <TabsTrigger value="create" className="flex items-center justify-center p-2 sm:p-4">
              <PlusSquare className="h-4 w-4 mr-2" />
              <span className="text-xs sm:text-sm">Create Rule</span>
            </TabsTrigger>
            <TabsTrigger value="combine" className="flex items-center justify-center p-2 sm:p-4">
              <Combine className="h-4 w-4 mr-2" />
              <span className="text-xs sm:text-sm">Combine Rules</span>
            </TabsTrigger>
            <TabsTrigger value="evaluate" className="flex items-center justify-center p-2 sm:p-4">
              <Play className="h-4 w-4 mr-2" />
              <span className="text-xs sm:text-sm">Evaluate Rules</span>
            </TabsTrigger>
          </TabsList>
          <TabsContent value="list"><RuleList /></TabsContent>
          <TabsContent value="create"><CreateRule /></TabsContent>
          <TabsContent value="combine"><CombineRules /></TabsContent>
          <TabsContent value="evaluate"><EvaluateRule /></TabsContent>
        </Tabs>
      </main>
    </div>
  );
};

export default RuleEngineDashboard;
